document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.getElementById('file-input');
  const preview = document.getElementById('preview');
  const analyzeBtn = document.getElementById('analyze-btn');
  const results = document.getElementById('results');
  const imageCountEl = document.getElementById('image-count');
  const timestampEl = document.getElementById('timestamp');
  const tableRisk = document.getElementById('table-risk');
  const tableSgr = document.getElementById('table-sgr');
  const recContent = document.getElementById('rec-content');
  const toast = document.getElementById('toast');
  const downloadZipBtn = document.getElementById('download-zip');
  const downloadRiskBtn = document.getElementById('download-risk');
  const downloadSgrBtn = document.getElementById('download-sgr');
  const downloadRecBtn = document.getElementById('download-rec');
  const healthStatus = document.getElementById('health-status');
  const spinner = document.getElementById('spinner');
  
  // 인증 관련 요소들
  const loginModal = document.getElementById('login-modal');
  const loginForm = document.getElementById('login-form');
  const closeLogin = document.getElementById('close-login');
  const userInfo = document.getElementById('user-info');
  const userName = document.getElementById('user-name');
  const logoutBtn = document.getElementById('logout-btn');
  
  // 피드백 관련 요소들
  const feedbackForm = document.getElementById('feedback-form');
  
  // 인증 상태
  let currentUser = null;
  let authToken = null;
  let currentSessionId = null;
  
  // SheetJS 로더 (CDN)
  let XLSXReady = null;
  async function ensureXLSX(){
    if(XLSXReady) return XLSXReady;
    XLSXReady = new Promise(async (resolve, reject) => {
      try{
        await import('https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js');
        resolve(window.XLSX);
      }catch(e){
        reject(e);
      }
    });
    return XLSXReady;
  }

  // 백엔드 주소 설정 (클라우드 배포 시 자동으로 환경변수에서 가져옴)
  const API_BASE = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://your-railway-app.railway.app'; // Railway 백엔드 URL로 수정 필요
  // 유틸: 토스트
  function showToast(msg){
    toast.textContent = msg;
    toast.classList.remove('hidden');
    clearTimeout(showToast._t);
    showToast._t = setTimeout(()=> toast.classList.add('hidden'), 2500);
  }

  // 유틸: 스피너 표시/숨김
  function showSpinner(){
    spinner.classList.remove('hidden');
    spinner.style.display = 'flex';
  }
  function hideSpinner(){
    spinner.classList.add('hidden');
    spinner.style.display = 'none';
  }

  // 인증 관련 함수들
  function showLoginModal() {
    loginModal.style.display = 'block';
  }
  
  function hideLoginModal() {
    loginModal.style.display = 'none';
  }
  
  function updateUserInterface() {
    if (currentUser) {
      userInfo.style.display = 'flex';
      userName.textContent = `${currentUser.full_name || currentUser.username} (${currentUser.organization || '베타 테스터'})`;
      loginModal.style.display = 'none';
    } else {
      userInfo.style.display = 'none';
      showLoginModal();
    }
  }
  
  async function login(username, password) {
    try {
      console.log('로그인 시도:', username);
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      
      console.log('API 요청 URL:', `${API_BASE}/auth/login`);
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        body: formData
      });
      
      console.log('응답 상태:', response.status);
      console.log('응답 OK:', response.ok);
      
      if (response.ok) {
        const data = await response.json();
        console.log('로그인 성공 데이터:', data);
        authToken = data.access_token;
        currentUser = data.user;
        
        // 토큰을 로컬 스토리지에 저장
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        updateUserInterface();
        hideLoginModal(); // 로그인 성공 시 모달 닫기
        showToast('로그인 성공!');
        return true;
      } else {
        const errorText = await response.text();
        console.log('로그인 실패 응답:', errorText);
        try {
          const error = JSON.parse(errorText);
          showToast(error.detail || '로그인 실패');
        } catch {
          showToast(`로그인 실패: ${response.status} ${response.statusText}`);
        }
        return false;
      }
    } catch (error) {
      console.error('로그인 오류:', error);
      showToast('로그인 중 오류가 발생했습니다: ' + error.message);
      return false;
    }
  }
  
  function logout() {
    authToken = null;
    currentUser = null;
    currentSessionId = null;
    
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    
    updateUserInterface();
    showToast('로그아웃되었습니다.');
  }
  
  function getAuthHeaders() {
    if (authToken) {
      return {
        'Authorization': `Bearer ${authToken}`
      };
    }
    return {};
  }
  
  // 페이지 초기화
  function initializePage(){
    // 스피너 숨기기
    hideSpinner();
    // 분석 버튼 비활성화
    analyzeBtn.disabled = true;
    // 결과 섹션 숨기기
    results.classList.add('hidden');
    // 파일 입력 초기화
    fileInput.value = '';
    // 미리보기 초기화
    preview.innerHTML = '';
    
    // 저장된 인증 정보 확인
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('currentUser');
    
    if (savedToken && savedUser) {
      authToken = savedToken;
      currentUser = JSON.parse(savedUser);
      updateUserInterface();
    } else {
      showLoginModal();
    }
  }

  // 이벤트 리스너 설정
  function setupEventListeners() {
    console.log('Setting up event listeners...');
    
    // 로그인 폼 제출
    if (loginForm) {
      console.log('Login form found, adding submit listener');
      loginForm.addEventListener('submit', async (e) => {
        console.log('Form submit event triggered');
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        console.log('Login attempt:', { username, password: password ? '***' : 'empty' });
        
        if (!username || !password) {
          showToast('사용자명과 비밀번호를 입력해주세요.');
          return;
        }
        
        const success = await login(username, password);
        if (success) {
          loginForm.reset();
        }
      });
    } else {
      console.error('Login form not found!');
    }

    // 로그인 모달 닫기
    closeLogin.addEventListener('click', () => {
      hideLoginModal();
    });

    // 로그인 버튼 클릭
    document.getElementById('login-btn').addEventListener('click', () => {
      showLoginModal();
    });

    // 로그아웃 버튼
    logoutBtn.addEventListener('click', logout);

    // 모달 외부 클릭 시 닫기
    window.addEventListener('click', (e) => {
      if (e.target === loginModal) {
        hideLoginModal();
      }
    });

    // ESC 키로 모달 닫기
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && loginModal.style.display === 'block') {
        hideLoginModal();
      }
    });

    // 탭 전환
    document.querySelectorAll('.tab').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        const key = btn.dataset.tab;
        document.getElementById(`tab-${key}`).classList.add('active');
      });
    });

    // 파일 미리보기
    fileInput.addEventListener('change', () => {
      preview.innerHTML = '';
      const files = Array.from(fileInput.files || []);
      if(files.length === 0){
        analyzeBtn.disabled = true;
        return;
      }
      analyzeBtn.disabled = false;
      files.forEach(file => {
        const reader = new FileReader();
        reader.onload = () => {
          const tpl = document.getElementById('preview-item-tpl');
          const node = tpl.content.cloneNode(true);
          const img = node.querySelector('img');
          const cap = node.querySelector('figcaption');
          img.src = reader.result;
          cap.textContent = file.name;
          preview.appendChild(node);
        };
        reader.readAsDataURL(file);
      });
    });

    // 분석 실행
    analyzeBtn.addEventListener('click', async () => {
      if (!currentUser) {
        showToast('로그인이 필요합니다.');
        showLoginModal();
        return;
      }
      
      const files = Array.from(fileInput.files || []);
      if(files.length === 0){
        showToast('이미지를 선택하세요.');
        return;
      }
      
      analyzeBtn.disabled = true;
      analyzeBtn.textContent = '분석 중...';
      showSpinner();
      
      try{
        const form = new FormData();
        files.forEach(f => form.append('files', f, f.name));
        form.append('session_name', `분석 세션 ${new Date().toLocaleString()}`);
        
        const res = await fetch(`${API_BASE}/analyze`, {
          method: 'POST',
          body: form,
          headers: getAuthHeaders()
        });
        
        if(!res.ok){
          if (res.status === 401) {
            showToast('인증이 만료되었습니다. 다시 로그인해주세요.');
            logout();
            return;
          }
          const err = await res.json().catch(()=>({detail:'오류'}));
          throw new Error(err.detail || '분석 오류');
        }
        
        const data = await res.json();

        // 세션 ID 저장 (피드백용)
        currentSessionId = data.session_id;

        // 메타
        imageCountEl.textContent = `총 이미지 수: ${data.image_count}장`;
        timestampEl.textContent = `생성 시간: ${data.timestamp}`;

        // 표 렌더링
        renderInnerTable(tableRisk, data.sections?.risk_analysis || '');
        renderInnerTable(tableSgr, data.sections?.sgr_checklist || '');
        recContent.textContent = data.sections?.recommendations || '';

        // 원문 저장
        const raw = data.full_report || '';
        lastSectionsRaw = splitSectionsRaw(raw);

        results.classList.remove('hidden');
        showToast('분석이 완료되었습니다.');
      }catch(e){
        console.error(e);
        showToast(e.message || '분석 중 오류 발생');
      }finally{
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = '📊 통합 분석 - 종합 위험성 평가서 생성';
        hideSpinner();
      }
    });

    // 다운로드 버튼들
    downloadRiskBtn.addEventListener('click', async () => {
      const ts = (timestampEl.textContent||'').replace('생성 시간: ','').replace(/[:\s-]/g,'').slice(0,14) || 'now';
      await downloadXLSFromTable(`위험요인분석_${ts}.xls`, tableRisk);
    });
    
    downloadSgrBtn.addEventListener('click', async () => {
      const ts = (timestampEl.textContent||'').replace('생성 시간: ','').replace(/[:\s-]/g,'').slice(0,14) || 'now';
      await downloadXLSFromTable(`SGR체크리스트_${ts}.xls`, tableSgr);
    });
    
    downloadRecBtn.addEventListener('click', async () => {
      const ts = (timestampEl.textContent||'').replace('생성 시간: ','').replace(/[:\s-]/g,'').slice(0,14) || 'now';
      const lines = (lastSectionsRaw.rec_raw || '내용이 없습니다.').split('\n');
      const aoa = [['추가 권장사항']].concat(lines.filter(Boolean).map(l => [l]));
      await downloadXLSFromAOA(`추가권장사항_${ts}.xls`, aoa);
    });
    
    downloadZipBtn.addEventListener('click', async () => {
      const ts = (timestampEl.textContent||'').replace('생성 시간: ','');
      await downloadZip(lastSectionsRaw, ts || new Date().toISOString());
    });
    
    // 피드백 제출
    feedbackForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      if (!currentUser) {
        showToast('로그인이 필요합니다.');
        return;
      }
      
      if (!currentSessionId) {
        showToast('분석 세션이 없습니다.');
        return;
      }
      
      const feedback = document.getElementById('feedback-text').value;
      const rating = document.querySelector('input[name="rating"]:checked')?.value;
      
      if (!rating) {
        showToast('만족도를 선택해주세요.');
        return;
      }
      
      if (!feedback.trim()) {
        showToast('피드백을 입력해주세요.');
        return;
      }
      
      try {
        const formData = new FormData();
        formData.append('feedback', feedback);
        formData.append('rating', rating);
        
        const response = await fetch(`${API_BASE}/feedback/${currentSessionId}`, {
          method: 'POST',
          body: formData,
          headers: getAuthHeaders()
        });
        
        if (response.ok) {
          showToast('피드백이 성공적으로 제출되었습니다. 감사합니다!');
          feedbackForm.reset();
        } else {
          const error = await response.json();
          showToast(error.detail || '피드백 제출에 실패했습니다.');
        }
      } catch (error) {
        showToast('피드백 제출 중 오류가 발생했습니다.');
      }
    });
  }

  // HTML 문자열을 테이블에 삽입
  function renderInnerTable(tableEl, innerHtml){
    tableEl.innerHTML = innerHtml || '';
  }

  // XLS 다운로드 유틸
  async function downloadXLSFromTable(filename, tableEl){
    try{
      const XLSX = await ensureXLSX();
      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.table_to_sheet(tableEl);
      XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
      XLSX.writeFile(wb, filename);
    }catch(e){
      console.error(e);
      showToast('XLS 생성 중 오류');
    }
  }
  
  async function downloadXLSFromAOA(filename, aoa){
    try{
      const XLSX = await ensureXLSX();
      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.aoa_to_sheet(aoa);
      XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
      XLSX.writeFile(wb, filename);
    }catch(e){
      console.error(e);
      showToast('XLS 생성 중 오류');
    }
  }

  // ZIP 다운로드
  async function downloadZip(sections, timestamp){
    try{
      const { default: JSZip } = await import('https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js');
      const zip = new JSZip();
      const stamp = timestamp.replace(/[:\s-]/g, '').slice(0,14);
      if(sections.risk_raw) zip.file(`1.위험요인분석_${stamp}.md`, new Blob([sections.risk_raw], {type:'text/markdown;charset=utf-8'}));
      if(sections.sgr_raw) zip.file(`2.체크리스트_${stamp}.md`, new Blob([sections.sgr_raw], {type:'text/markdown;charset=utf-8'}));
      if(sections.rec_raw) zip.file(`4.추가권장사항_${stamp}.md`, new Blob([sections.rec_raw], {type:'text/markdown;charset=utf-8'}));
      const blob = await zip.generateAsync({type:'blob'});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `전체섹션_${stamp}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    }catch(e){
      showToast('ZIP 생성 중 오류가 발생했습니다.');
    }
  }

  let lastSectionsRaw = { risk_raw:'', sgr_raw:'', rec_raw:'' };

  // 원문에서 섹션 간단 추출
  function splitSectionsRaw(text){
    const lines = text.split('\n');
    let cur = '';
    const out = { risk_raw:'', sgr_raw:'', rec_raw:'' };
    for(const line of lines){
      if(line.includes('위험요인') || line.includes('잠재 위험')) cur = 'risk_raw';
      else if(line.includes('체크리스트') || line.includes('SGR')) cur = 'sgr_raw';
      else if(line.includes('권장사항') || line.includes('추가 권장')) cur = 'rec_raw';
      if(cur) out[cur] += line + '\n';
    }
    return out;
  }

  // 헬스체크
  async function checkHealth(){
    try{
      const res = await fetch(`${API_BASE}/health`, {cache:'no-store'});
      const data = await res.json();
      if(data.status === 'healthy'){
        healthStatus.textContent = '백엔드 연결됨';
      } else {
        healthStatus.textContent = '백엔드 비정상';
      }
    }catch{
      healthStatus.textContent = '백엔드 연결 실패';
    }
  }

  // 초기화
  function init() {
    console.log('Initializing application...');
    console.log('Login form element:', loginForm);
    console.log('Login modal element:', loginModal);
    console.log('Close login element:', closeLogin);
    
    setupEventListeners();
    initializePage();
    checkHealth();
    
    console.log('Initialization complete');
  }

  // 페이지 로드 시 초기화
  init();
});


