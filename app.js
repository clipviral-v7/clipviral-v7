const $ = selector => document.querySelector(selector);
const video = $('#video'), file = $('#file'), drop = $('#drop');
const start = $('#start'), end = $('#end'), seek = $('#seek'), overlay = $('#overlay');
let duration = 0, titleColor = '#8b6cff', uploadedFile;
const fmt = value => `${String(Math.floor(value / 60)).padStart(2, '0')}:${String(Math.floor(value % 60)).padStart(2, '0')}`;

function setNote(message) { $('#note').textContent = message; }
function loadVideo(item) {
  if (!item || !item.type.startsWith('video/')) return setNote('Elige un archivo de vídeo válido.');
  uploadedFile = item;
  video.src = URL.createObjectURL(item);
  $('#empty').style.display = 'none';
  $('#fileLabel').textContent = item.name;
  setNote('Vídeo cargado. Analizando momentos con IA…');
  analyzeVideo(item);
}

async function analyzeVideo(item) {
  const form = new FormData();
  form.append('video', item);
  try {
    const response = await fetch('/api/analyze', { method: 'POST', body: form });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'No se pudo analizar el vídeo.');
    renderSuggestions(data.clips || []);
  } catch (error) {
    setNote(error.message + ' Puedes marcar el corte manualmente mientras tanto.');
  }
}

function renderSuggestions(clips) {
  let box = $('#suggestions');
  if (!box) { box = document.createElement('div'); box.id = 'suggestions'; box.style.marginTop = '14px'; $('.analysis').after(box); }
  if (!clips.length) { setNote('No encontramos momentos claros. Prueba con otro vídeo.'); return; }
  box.innerHTML = '<p style="font:11px DM Mono;color:#aaa;margin:0 0 8px">CLIPS SUGERIDOS POR IA</p>';
  clips.forEach((clip, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.style.cssText = 'width:100%;text-align:left;margin:0 0 7px;padding:10px;border:1px solid #48474f;border-radius:7px;background:#29292f;color:white;font:12px Manrope;cursor:pointer';
    button.innerHTML = `<b>${clip.score}% viral</b><br><span style="color:#bbb">${fmt(clip.start)}–${fmt(clip.end)} · ${clip.title}</span>`;
    button.onclick = () => selectClip(clip);
    box.appendChild(button);
    if (index === 0) selectClip(clip);
  });
  setNote('Elige una sugerencia para generar y descargar tu clip.');
}

function selectClip(clip) {
  start.value = clip.start; end.value = Math.min(duration || clip.end, clip.end);
  $('#startText').textContent = fmt(start.value); $('#endText').textContent = fmt(end.value);
  $('#clipTitle').value = clip.title; overlay.textContent = clip.title;
  document.querySelector('.score').textContent = `${clip.score}%`; document.querySelector('.meter b').style.width = `${clip.score}%`;
  video.currentTime = clip.start; $('#download').disabled = false;
}

$('#choose').onclick = () => file.click();
file.onchange = () => loadVideo(file.files[0]);
['dragenter', 'dragover'].forEach(event => drop.addEventListener(event, e => { e.preventDefault(); drop.style.borderColor = '#d1ff00'; }));
drop.ondragleave = () => drop.style.borderColor = '';
drop.ondrop = event => { event.preventDefault(); drop.style.borderColor = ''; loadVideo(event.dataTransfer.files[0]); };

video.onloadedmetadata = () => {
  duration = video.duration;
  [start, end, seek].forEach(input => input.max = duration);
  end.value = duration; $('#duration').textContent = fmt(duration); $('#endText').textContent = fmt(duration);
};
video.ontimeupdate = () => {
  seek.value = video.currentTime; $('#current').textContent = fmt(video.currentTime);
  if (video.currentTime >= Number(end.value)) { video.pause(); video.currentTime = Number(start.value); }
};
start.oninput = () => { if (Number(start.value) >= Number(end.value)) end.value = Number(start.value) + .1; $('#startText').textContent = fmt(start.value); video.currentTime = start.value; };
end.oninput = () => { if (Number(end.value) <= Number(start.value)) start.value = Math.max(0, Number(end.value) - .1); $('#endText').textContent = fmt(end.value); };
seek.oninput = () => video.currentTime = seek.value;
$('#play').onclick = () => { if (!video.src) return; if (video.currentTime < Number(start.value) || video.currentTime >= Number(end.value)) video.currentTime = start.value; video.paused ? video.play() : video.pause(); };
$('#reset').onclick = () => { start.value = 0; end.value = duration; start.dispatchEvent(new Event('input')); end.dispatchEvent(new Event('input')); };
$('#clipTitle').oninput = event => overlay.textContent = event.target.value;
document.querySelectorAll('.colors button').forEach(button => button.onclick = () => { document.querySelectorAll('.colors button').forEach(item => item.classList.remove('selected')); button.classList.add('selected'); titleColor = button.dataset.color; overlay.style.color = titleColor; });

$('#download').onclick = async () => {
  if (!video.src) return;
  const button = $('#download'); button.disabled = true; button.textContent = 'Generando clip…'; setNote('Generando tu archivo, no cierres esta pestaña.');
  const canvas = document.createElement('canvas'), context = canvas.getContext('2d'); canvas.width = 1280; canvas.height = 720;
  const stream = canvas.captureStream(30);
  if (video.captureStream) video.captureStream().getAudioTracks().forEach(track => stream.addTrack(track));
  const recorder = new MediaRecorder(stream, { mimeType: MediaRecorder.isTypeSupported('video/webm;codecs=vp9,opus') ? 'video/webm;codecs=vp9,opus' : 'video/webm' });
  const chunks = []; recorder.ondataavailable = event => chunks.push(event.data);
  recorder.onstop = () => { const link = document.createElement('a'); link.href = URL.createObjectURL(new Blob(chunks, { type: 'video/webm' })); link.download = `clipping-${Date.now()}.webm`; link.click(); button.disabled = false; button.textContent = 'Generar y descargar clip'; setNote('¡Clip generado y descargado!'); };
  recorder.start(); video.currentTime = Number(start.value); await video.play();
  function draw() {
    context.fillStyle = '#000'; context.fillRect(0, 0, 1280, 720);
    const ratio = Math.min(1280 / video.videoWidth, 720 / video.videoHeight), width = video.videoWidth * ratio, height = video.videoHeight * ratio;
    context.drawImage(video, (1280 - width) / 2, (720 - height) / 2, width, height);
    context.font = '800 42px sans-serif'; context.textAlign = 'center'; context.lineWidth = 6; context.strokeStyle = 'rgba(0,0,0,.7)'; context.strokeText($('#clipTitle').value, 640, 655); context.fillStyle = titleColor; context.fillText($('#clipTitle').value, 640, 655);
    if (video.currentTime < Number(end.value)) requestAnimationFrame(draw); else { video.pause(); recorder.stop(); }
  }
  draw();
};
