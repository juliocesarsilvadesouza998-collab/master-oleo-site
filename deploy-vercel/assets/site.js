'use strict';
document.documentElement.classList.add('js');
document.documentElement.classList.remove('no-js');
const menuButton=document.querySelector('[data-menu-toggle]');
const menu=document.getElementById('site-nav');
function closeMenu(restore=false){if(!menuButton||!menu)return;menu.classList.remove('is-open');menuButton.setAttribute('aria-expanded','false');if(restore)menuButton.focus();}
if(menuButton&&menu){menuButton.hidden=false;menuButton.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));menu.classList.toggle('is-open',open);});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.classList.contains('is-open'))closeMenu(true);});document.addEventListener('click',e=>{if(!e.target.closest('.header'))closeMenu();});menu.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});window.matchMedia('(min-width:861px)').addEventListener('change',e=>{if(e.matches)closeMenu();});}

const calc=document.querySelector('[data-calculator]');
function updateCalculation(){
 if(!calc)return true;
 const volume=calc.querySelector('[name=volume_litros]');const quality=calc.querySelector('[name=qualidade]');
 const liters=Number(volume.value);const price=Number(quality.selectedOptions[0].dataset.price);
 const valid=volume.value.trim()!==''&&Number.isFinite(liters)&&liters>=1&&liters<=1000000;
 volume.setCustomValidity(valid?'':'Informe um volume entre 1 e 1.000.000 de litros.');
 const msg=calc.querySelector('[data-calc-error]');msg.hidden=valid;volume.setAttribute('aria-invalid',String(!valid));
 const monthly=document.getElementById('monthly');const annual=document.getElementById('annual');
 if(!valid){monthly.value='—';annual.textContent='Informe um volume válido para calcular.';calc.querySelector('[name=valor_estimado]').value='';return false;}
 const format=v=>v.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
 monthly.value=format(liters*price);annual.textContent=format(liters*price*12)+' por ano, se o volume se mantiver.';
 calc.querySelector('[name=preco_referencia]').value=price.toFixed(2)+' BRL/L';
 calc.querySelector('[name=valor_estimado]').value=format(liters*price)+'/mês';return true;
}
if(calc){calc.querySelector('[name=volume_litros]').addEventListener('input',updateCalculation);calc.querySelector('[name=qualidade]').addEventListener('change',updateCalculation);updateCalculation();}

function track(name,detail={}){document.dispatchEvent(new CustomEvent('masteroleo:analytics',{detail:{event:name,...detail}}));}
document.querySelectorAll('a[href^="https://wa.me/"]').forEach(a=>a.addEventListener('click',()=>track('whatsapp_click',{page:location.pathname})));
for(const form of document.querySelectorAll('[data-lead-form]')){
 let started=false;form.addEventListener('input',()=>{if(!started){track('form_start',{page:location.pathname});started=true;}},{passive:true});
 form.addEventListener('submit',async e=>{
  e.preventDefault();if(form===calc&&!updateCalculation()){form.reportValidity();return;}if(!form.reportValidity())return;
  const status=form.querySelector('[data-form-status]');const button=form.querySelector('button[type=submit]');const original=button.textContent;
  const fd=new FormData(form);if(fd.get('_gotcha'))return;
  button.disabled=true;button.textContent='Enviando…';form.setAttribute('aria-busy','true');status.classList.remove('error');status.textContent='Enviando sua solicitação.';
  const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),15000);
  try{
   const response=await fetch(form.action,{method:'POST',body:fd,headers:{Accept:'application/json'},signal:controller.signal});
   if(!response.ok)throw new Error('request_failed');
   status.textContent='Solicitação recebida. A equipe Master Óleo retornará pelo contato informado.';
   track('form_success',{page:location.pathname});form.reset();if(form===calc)updateCalculation();started=false;
  }catch{
   status.classList.add('error');status.textContent='Não foi possível confirmar o envio. Seus dados foram mantidos. Tente novamente ou use o link de WhatsApp abaixo.';
   track('form_error',{page:location.pathname});
  }finally{clearTimeout(timeout);button.disabled=false;button.textContent=original;form.removeAttribute('aria-busy');}
 });
}
// Preserve access from older bookmarked sections without retaining a long home page.
if(document.body.dataset.page==='index.html'){
 const legacy={contato:'contato.html',calculadora:'calculadora.html',quem:'industrias.html',industrias:'industrias.html',blog:'blog/',faq:'servicos.html',prova:'servicos.html','prova-social':'servicos.html','nicho-maquinas':'oleo-vegetal-industrial.html'};
 const target=legacy[location.hash.slice(1)];if(target)location.replace(target);
}
