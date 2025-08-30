
document.addEventListener("DOMContentLoaded", function(){
  try{
    VANTA.NET({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.0,
      color: 0x7c4dff,
      backgroundColor: 0x05050a,
      spacing: 20.00,
      showDots: true
    });
  }catch(e){
    console.warn("Vanta init failed:", e);
  }
  const btn = document.getElementById('btn-refresh');
  if(btn) btn.addEventListener('click', ()=> location.reload());
});

function filterTable(){
  const q = document.getElementById('search-input').value.toLowerCase();
  const rows = document.querySelectorAll('#contacts-table tbody tr');
  rows.forEach(r => {
    const name = r.cells[0]?.innerText.toLowerCase() || '';
    const num = r.cells[1]?.innerText || '';
    if(name.includes(q) || num.includes(q)) r.style.display = '';
    else r.style.display = 'none';
  });
}

function closeModal(e){
  if(e.target.classList.contains('modal')){
    e.target.classList.remove('show');
  }
}
