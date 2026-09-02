import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vanguard Tactical 3D",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100% !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    if "game_started" not in st.session_state:
        st.session_state.game_started = False

    if not st.session_state.game_started:
        st.title("🎯 Vanguard Tactical (Streamlit 3D FPS)")
        st.subheader("메인 메뉴")
        st.write("1인칭 전술 슈팅 웹게임입니다.")
        st.markdown("""
        **조작법 및 신규 기능:**
        - **사격**: 마우스 좌클릭 / `E` 키
        - **점프**: `Space` 키 | **달리기**: `Shift` 키
        - **라운드 스킵**: `M` 키 (즉시 다음 라운드로 이동)
        - **전체 화면 전환**: `O` 키
        - **상점 열기/닫기**: `B` 키 (산탄총 150G / 기관총 300G)
        - **이동**: WASD | **재장전**: R | **무기 교체**: 1, 2, 3, 4 키
        - **몬스터 디테일 업**: 디테일한 장갑과 빛나는 눈을 가진 디테일한 3D 적 모델 적용!
        - **보스전**: **5라운드**마다 거대 타이탄 등장! (내려찍기 & 충격파 주의)
        """)
        
        if st.button("게임 시작", type="primary", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
    else:
        game_html = """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <style>
                html, body {
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                    overflow: hidden;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    user-select: none;
                    background-color: #05050a;
                }
                #game-container {
                    width: 100vw;
                    height: 100vh;
                    position: relative;
                    cursor: none;
                }
                #hud {
                    position: absolute;
                    top: 15px;
                    left: 20px;
                    color: #00ffcc;
                    font-size: 18px;
                    font-weight: bold;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
                    pointer-events: none;
                    z-index: 10;
                }
                #boss-hud {
                    display: none;
                    position: absolute;
                    top: 55px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 50%;
                    background: rgba(0, 0, 0, 0.7);
                    border: 2px solid #ff0055;
                    border-radius: 8px;
                    padding: 8px 15px;
                    text-align: center;
                    color: #ff0055;
                    font-weight: bold;
                    z-index: 10;
                }
                #boss-hp-bar {
                    width: 100%;
                    height: 16px;
                    background: #333;
                    border-radius: 4px;
                    margin-top: 5px;
                    overflow: hidden;
                }
                #boss-hp-fill {
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, #ff0055, #ff5500);
                    transition: width 0.1s linear;
                }
                #crosshair {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 20px;
                    height: 20px;
                    transform: translate(-50%, -50%);
                    pointer-events: none;
                    z-index: 10;
                }
                #crosshair::before {
                    content: '';
                    position: absolute;
                    top: 9px;
                    left: 0;
                    width: 20px;
                    height: 2px;
                    background: #00ffcc;
                    box-shadow: 0 0 6px #00ffcc;
                }
                #crosshair::after {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 9px;
                    width: 2px;
                    height: 20px;
                    background: #00ffcc;
                    box-shadow: 0 0 6px #00ffcc;
                }
                #muzzle-flash-hud {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 60px;
                    height: 60px;
                    transform: translate(-50%, -50%);
                    background: radial-gradient(circle, rgba(255,230,120,0.8) 0%, rgba(255,100,0,0.4) 40%, rgba(0,0,0,0) 70%);
                    pointer-events: none;
                    z-index: 9;
                    display: none;
                    border-radius: 50%;
                }
                
                #top-controls {
                    position: absolute;
                    top: 15px;
                    right: 20px;
                    z-index: 15;
                    display: flex;
                    gap: 10px;
                }
                .ui-btn {
                    padding: 10px 18px;
                    font-size: 15px;
                    font-weight: bold;
                    color: #111;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.5);
                }
                #shop-btn { background-color: #ffd700; }
                #fullscreen-btn { background-color: #00ffcc; }

                #start-overlay {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: white;
                    text-align: center;
                    background: rgba(10, 10, 20, 0.9);
                    padding: 30px 50px;
                    border-radius: 12px;
                    z-index: 20;
                    border: 2px solid #00ffcc;
                    cursor: default;
                }
                #start-btn {
                    margin-top: 15px;
                    padding: 12px 30px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #111;
                    background-color: #00ffcc;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                }
                #shop-modal {
                    display: none;
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: rgba(15, 15, 25, 0.95);
                    border: 2px solid #ffd700;
                    padding: 25px;
                    border-radius: 12px;
                    color: white;
                    z-index: 25;
                    min-width: 340px;
                    text-align: center;
                    cursor: default;
                }
                .buy-item {
                    margin: 12px 0;
                    padding: 10px;
                    background: rgba(255,255,255,0.05);
                    border-radius: 6px;
                    text-align: left;
                }
                .buy-btn {
                    margin-top: 6px;
                    padding: 8px 16px;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: bold;
                    width: 100%;
                }
                .buy-btn:disabled {
                    background-color: #555;
                    cursor: not-allowed;
                }
                #game-over {
                    display: none;
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: #ff3333;
                    font-size: 36px;
                    text-align: center;
                    background: rgba(0, 0, 0, 0.92);
                    padding: 40px;
                    border-radius: 12px;
                    z-index: 30;
                    cursor: default;
                    border: 2px solid #ff3333;
                }
            </style>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        </head>
        <body>
            <div id="game-container">
                <div id="hud">
                    라운드: <span id="round">1</span> | 
                    체력: <span id="health" style="color: #00ffcc;">100</span> | 
                    골드: <span id="money" style="color:#ffd700;">0</span>G | 
                    무기: <span id="weapon">권총</span> | 
                    탄약: <span id="ammo">12 / 12</span> | 
                    처치: <span id="kills">0</span> | 
                    남은 적: <span id="enemies-left">0</span>
                </div>

                <div id="boss-hud">
                    ⚠️ 보스 : <span id="boss-title">크로노스 타이탄</span>
                    <div id="boss-hp-bar"><div id="boss-hp-fill"></div></div>
                </div>

                <div id="crosshair"></div>
                <div id="muzzle-flash-hud"></div>
                
                <div id="top-controls">
                    <button id="shop-btn" class="ui-btn" onclick="toggleShop()">🛒 상점 (B)</button>
                    <button id="fullscreen-btn" class="ui-btn" onclick="toggleFullScreen()">🖥️ 전체 화면 (O)</button>
                </div>

                <div id="shop-modal">
                    <h2 style="color: #ffd700; margin-top:0;">무기 상점</h2>
                    <p>현재 보유 골드: <span id="shop-money" style="color: #ffd700; font-weight: bold;">0</span>G</p>
                    <hr style="border-color: #444;">
                    
                    <div class="buy-item">
                        <h4 style="margin: 0; color: #ff8800;">💥 산탄총 (Shotgun)</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">근거리 8발 동시 발사 | 탄창: 6발</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 150G</p>
                        <button id="buy-sg-btn" class="buy-btn" onclick="buyWeapon(3)">산탄총 구매 (150G)</button>
                    </div>

                    <div class="buy-item">
                        <h4 style="margin: 0; color: #ffd700;">🔫 기관총 (LMG)</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">초고속 연사 | 탄창: 100발</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 300G</p>
                        <button id="buy-lmg-btn" class="buy-btn" onclick="buyWeapon(4)">기관총 구매 (300G)</button>
                    </div>

                    <button onclick="toggleShop()" style="margin-top: 10px; padding: 6px 20px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">닫기</button>
                </div>
                
                <div id="start-overlay">
                    <h2>🎯 게임 준비 완료</h2>
                    <p style="color: #ccc; margin-bottom: 5px;">전투를 시작하려면 버튼을 누르세요.</p>
                    <button id="start-btn" onclick="startGame()">전투 시작</button>
                </div>

                <div id="game-over">
                    <h1 id="game-over-title">게임 오버</h1>
                    <p id="game-over-desc" style="font-size: 18px; color: #fff; margin-bottom: 20px;"></p>
                    <button id="game-over-btn" onclick="resetOrNextRound()" style="font-size: 20px; padding: 10px 25px; cursor: pointer; background: #00ffcc; border: none; border-radius: 6px; font-weight: bold;">다음 라운드</button>
                </div>
            </div>

            <script>
                let audioCtx = null;
                
                function initAudio() {
                    if (!audioCtx) {
                        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    }
                    if (audioCtx.state === 'suspended') {
                        audioCtx.resume();
                    }
                }

                function playGunSound(type) {
                    initAudio();
                    if (!audioCtx) return;

                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    
                    if (type === 1) {
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(320, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.12);
                        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
                    } else if (type === 2) {
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(240, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.15);
                        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
                    } else if (type === 3) {
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(120, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.25);
                        gain.gain.setValueAtTime(0.7, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
                    } else if (type === 4) {
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(180, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(35, audioCtx.currentTime + 0.08);
                        gain.gain.setValueAtTime(0.6, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
                    } else if (type === 'slam') {
                        osc.type = 'triangle';
                        osc.frequency.setValueAtTime(100, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 0.5);
                        gain.gain.setValueAtTime(1.0, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                    }
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.5);
                }

                const WEAPONS = {
                    1: { name: '권총', damage: 25, range: 40, fireRate: 280, magSize: 12, reloadTime: 1200, recoil: 0.02, owned: true },
                    2: { name: '소총', damage: 55, range: 60, fireRate: 120, magSize: 30, reloadTime: 2000, recoil: 0.04, owned: true },
                    3: { name: '산탄총', damage: 18, range: 18, fireRate: 750, magSize: 6, reloadTime: 2400, recoil: 0.1, pellets: 8, owned: false, price: 150 },
                    4: { name: '기관총', damage: 65, range: 70, fireRate: 80, magSize: 100, reloadTime: 3000, recoil: 0.03, owned: false, price: 300 }
                };

                let round = 1, kills = 0, money = 0, playerHealth = 150;
                let isMouseDown = false;
                let bossAttackIndex = 0;
                let currentWeaponId = 1, currentAmmo = WEAPONS[1].magSize;
                let isReloading = false, lastShotTime = 0;

                let scene, camera, renderer, gunMesh, muzzleLight;
                let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false, isSprinting = false;
                
                let playerVelocityY = 0;
                let isGrounded = true;
                const GRAVITY = -28.0;
                const JUMP_FORCE = 10.0;
                const PLAYER_HEIGHT = 1.6;

                let prevTime = performance.now();
                let velocity = new THREE.Vector3(), direction = new THREE.Vector3();
                let enemies = [], shockwaves = [], isGameActive = false, isShopOpen = false;
                let isRoundCleared = false;
                let roundRewardGiven = false;
                let bossEnemy = null;

                let pitch = 0, yaw = 0;

                const startOverlay = document.getElementById('start-overlay');
                const gameOverScreen = document.getElementById('game-over');

                function init() {
                    scene = new THREE.Scene();
                    scene.background = new THREE.Color(0x050510);
                    scene.fog = new THREE.FogExp2(0x050510, 0.02);

                    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                    camera.position.y = PLAYER_HEIGHT;

                    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
                    scene.add(ambientLight);

                    const dirLight = new THREE.DirectionalLight(0x00ffff, 0.8);
                    dirLight.position.set(20, 40, 20);
                    scene.add(dirLight);

                    muzzleLight = new THREE.PointLight(0xffaa00, 0, 10);
                    scene.add(muzzleLight);

                    renderer = new THREE.WebGLRenderer({ antialias: true });
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    const container = document.getElementById('game-container');
                    container.appendChild(renderer.domElement);

                    createGunModel();

                    container.addEventListener('mousemove', (e) => {
                        if (!isGameActive || isShopOpen) return;

                        yaw -= e.movementX * 0.0025;
                        pitch -= e.movementY * 0.0025;
                        pitch = Math.max(-Math.PI / 2 + 0.1, Math.min(Math.PI / 2 - 0.1, pitch));

                        camera.rotation.order = "YXZ";
                        camera.rotation.y = yaw;
                        camera.rotation.x = pitch;
                    });

                    container.addEventListener('mousedown', (e) => {
                        initAudio();
                        if (isShopOpen) return;
                        if (isGameActive && e.button === 0) {
                            isMouseDown = true;
                            if (!isReloading) shoot();
                        }
                    });
                    container.addEventListener('mouseup', (e) => {
                        if (e.button === 0) isMouseDown = false;
                    });
                    container.addEventListener('mouseleave', () => {
                        isMouseDown = false;
                    });

                    document.addEventListener('keydown', onKeyDown);
                    document.addEventListener('keyup', onKeyUp);

                    window.addEventListener('resize', onWindowResize);

                    buildMap();
                    startRound();
                    animate();
                }

                function onWindowResize() {
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                }

                function toggleFullScreen() {
                    const container = document.getElementById('game-container');
                    if (!document.fullscreenElement) {
                        container.requestFullscreen().catch(err => {
                            alert(`전체 화면 전환 실패: ${err.message}`);
                        });
                    } else {
                        document.exitFullscreen();
                    }
                }

                function createGunModel() {
                    if (gunMesh) camera.remove(gunMesh);

                    const gunGroup = new THREE.Group();

                    if (currentWeaponId === 4) {
                        const bodyGeo = new THREE.BoxGeometry(0.18, 0.2, 0.85);
                        const bodyMat = new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 0.9, roughness: 0.1 });
                        const body = new THREE.Mesh(bodyGeo, bodyMat);
                        body.position.set(0.22, -0.2, -0.5);

                        const magGeo = new THREE.BoxGeometry(0.14, 0.25, 0.22);
                        const magMat = new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.5 });
                        const mag = new THREE.Mesh(magGeo, magMat);
                        mag.position.set(0.22, -0.32, -0.45);

                        gunGroup.add(body);
                        gunGroup.add(mag);
                    } else if (currentWeaponId === 3) {
                        const barrelGeo = new THREE.CylinderGeometry(0.06, 0.06, 0.7, 8);
                        const barrelMat = new THREE.MeshStandardMaterial({ color: 0xff6600, metalness: 0.8, roughness: 0.2 });
                        const barrel = new THREE.Mesh(barrelGeo, barrelMat);
                        barrel.rotation.x = Math.PI / 2;
                        barrel.position.set(0.2, -0.2, -0.5);

                        const stockGeo = new THREE.BoxGeometry(0.1, 0.12, 0.3);
                        const stockMat = new THREE.MeshStandardMaterial({ color: 0x552200 });
                        const stock = new THREE.Mesh(stockGeo, stockMat);
                        stock.position.set(0.2, -0.22, -0.2);

                        gunGroup.add(barrel);
                        gunGroup.add(stock);
                    } else if (currentWeaponId === 2) {
                        const barrelGeo = new THREE.BoxGeometry(0.1, 0.12, 0.65);
                        const barrelMat = new THREE.MeshStandardMaterial({ color: 0x00ffcc, metalness: 0.8, roughness: 0.2 });
                        const barrel = new THREE.Mesh(barrelGeo, barrelMat);
                        barrel.position.set(0.2, -0.2, -0.45);

                        gunGroup.add(barrel);
                    } else {
                        const slideGeo = new THREE.BoxGeometry(0.08, 0.1, 0.35);
                        const slideMat = new THREE.MeshStandardMaterial({ color: 0xffffff, metalness: 0.9, roughness: 0.1 });
                        const slide = new THREE.Mesh(slideGeo, slideMat);
                        slide.position.set(0.2, -0.2, -0.35);

                        const handleGeo = new THREE.BoxGeometry(0.07, 0.18, 0.1);
                        const handleMat = new THREE.MeshStandardMaterial({ color: 0x222222 });
                        const handle = new THREE.Mesh(handleGeo, handleMat);
                        handle.position.set(0.2, -0.3, -0.28);
                        handle.rotation.x = -0.2;

                        gunGroup.add(slide);
                        gunGroup.add(handle);
                    }

                    gunMesh = gunGroup;
                    camera.add(gunMesh);
                    scene.add(camera);
                }

                function startGame() {
                    initAudio();
                    startOverlay.style.display = 'none';
                    isGameActive = true;
                }

                function toggleShop() {
                    isShopOpen = !isShopOpen;
                    const modal = document.getElementById('shop-modal');
                    modal.style.display = isShopOpen ? 'block' : 'none';
                    document.getElementById('shop-money').innerText = money;
                    
                    const buySgBtn = document.getElementById('buy-sg-btn');
                    if (WEAPONS[3].owned) {
                        buySgBtn.innerText = '보유 중 (3번 키로 장착)';
                        buySgBtn.disabled = true;
                    } else {
                        buySgBtn.disabled = money < WEAPONS[3].price;
                    }

                    const buyLmgBtn = document.getElementById('buy-lmg-btn');
                    if (WEAPONS[4].owned) {
                        buyLmgBtn.innerText = '보유 중 (4번 키로 장착)';
                        buyLmgBtn.disabled = true;
                    } else {
                        buyLmgBtn.disabled = money < WEAPONS[4].price;
                    }
                }

                function buyWeapon(id) {
                    const w = WEAPONS[id];
                    if (money >= w.price && !w.owned) {
                        money -= w.price;
                        w.owned = true;
                        switchWeapon(id);
                        toggleShop();
                        updateHUD();
                    }
                }

                function skipRound() {
                    if (!isGameActive) return;
                    endGame(true);
                }

                function buildMap() {
                    const gridHelper = new THREE.GridHelper(100, 50, 0x00ffcc, 0x333355);
                    gridHelper.position.y = 0.01;
                    scene.add(gridHelper);

                    const floorGeo = new THREE.PlaneGeometry(100, 100);
                    const floorMat = new THREE.MeshStandardMaterial({ color: 0x0a0a18, roughness: 0.5 });
                    const floor = new THREE.Mesh(floorGeo, floorMat);
                    floor.rotation.x = -Math.PI / 2;
                    scene.add(floor);

                    const createWall = (w, h, d, x, y, z, colorHex) => {
                        const geo = new THREE.BoxGeometry(w, h, d);
                        const mat = new THREE.MeshStandardMaterial({ color: colorHex, metalness: 0.6, roughness: 0.2 });
                        const mesh = new THREE.Mesh(geo, mat);
                        mesh.position.set(x, y, z);
                        
                        const edges = new THREE.EdgesGeometry(geo);
                        const line = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0x00ffcc }));
                        mesh.add(line);

                        scene.add(mesh);
                    };

                    createWall(100, 10, 2, 0, 5, -50, 0x112233);
                    createWall(100, 10, 2, 0, 5, 50, 0x112233);
                    createWall(2, 10, 100, -50, 5, 0, 0x112233);
                    createWall(2, 10, 100, 50, 5, 0, 0x112233);

                    createWall(20, 6, 4, -15, 3, -10, 0x440066);
                    createWall(4, 6, 20, 15, 3, 10, 0x663300);
                    createWall(12, 6, 12, 0, 3, 0, 0x004466);
                }

                function startRound() {
                    enemies.forEach(e => scene.remove(e.mesh));
                    enemies = [];
                    bossEnemy = null;
                    
                    shockwaves.forEach(s => scene.remove(s.mesh));
                    shockwaves = [];

                    playerHealth = 150;
                    roundRewardGiven = false;
                    camera.position.set(0, PLAYER_HEIGHT, 40);
                    
                    document.getElementById('boss-hud').style.display = 'none';

                    if (round % 5 === 0) {
                        createBossEnemy(0, -20);
                        document.getElementById('boss-hud').style.display = 'block';
                    } else {
                        const enemyCount = round * 2 + 1;
                        const spawnPositions = [
                            {x: -30, z: -30}, {x: 0, z: -35}, {x: 30, z: -30},
                            {x: -25, z: 0}, {x: 25, z: 0}
                        ];

                        for (let i = 0; i < enemyCount; i++) {
                            const pos = spawnPositions[i % spawnPositions.length];
                            createEnemy(pos.x + (Math.random()*4 - 2), pos.z + (Math.random()*4 - 2));
                        }
                    }
                    updateHUD();
                }

                // 웅장한 디테일 3D 몬스터 세동
                function createEnemy(x, z) {
                    const group = new THREE.Group();

                    // 1. 역삼각형의 중장갑 가슴
                    const torsoGeo = new THREE.ConeGeometry(0.8, 1.4, 6);
                    const armorMat = new THREE.MeshStandardMaterial({ color: 0x331122, metalness: 0.8, roughness: 0.3 });
                    const torso = new THREE.Mesh(torsoGeo, armorMat);
                    torso.rotation.x = Math.PI;
                    torso.position.y = 1.3;
                    group.add(torso);

                    // 2. 어깨 갑옷
                    const shoulderGeo = new THREE.BoxGeometry(1.6, 0.4, 0.6);
                    const shoulderMat = new THREE.MeshStandardMaterial({ color: 0x880022, metalness: 0.9, roughness: 0.2 });
                    const shoulder = new THREE.Mesh(shoulderGeo, shoulderMat);
                    shoulder.position.y = 1.8;
                    group.add(shoulder);

                    // 3. 투구 및 가시 머리
                    const headGeo = new THREE.OctahedronGeometry(0.4, 0);
                    const headMat = new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.9 });
                    const head = new THREE.Mesh(headGeo, headMat);
                    head.position.y = 2.2;
                    group.add(head);

                    // 4. 빛나는 붉은 안광 (Eye glow)
                    const eyeGeo = new THREE.BoxGeometry(0.3, 0.08, 0.1);
                    const eyeMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
                    const eye = new THREE.Mesh(eyeGeo, eyeMat);
                    eye.position.set(0, 2.2, -0.3);
                    group.add(eye);

                    group.position.set(x, 0, z);
                    scene.add(group);

                    enemies.push({
                        mesh: group,
                        hp: 50 + (round * 10),
                        maxHp: 50 + (round * 10),
                        speed: 3 + (Math.random() * 1.5),
                        damage: 10,
                        lastAttack: 0,
                        isBoss: false
                    });
                }

                // 거대 웅장한 보스 몬스터
                function createBossEnemy(x, z) {
                    const group = new THREE.Group();

                    // 거대한 용 보스: 몸통, 긴 목, 턱, 뿔, 날개, 다리, 꼬리, 등가시
                    const skinMat = new THREE.MeshStandardMaterial({ color: 0x6b1020, metalness: 0.25, roughness: 0.5, emissive: 0x220006, emissiveIntensity: 0.25 });
                    const scaleMat = new THREE.MeshStandardMaterial({ color: 0x9d2034, metalness: 0.15, roughness: 0.62 });
                    const wingMat = new THREE.MeshStandardMaterial({ color: 0x260812, metalness: 0.1, roughness: 0.7, side: THREE.DoubleSide });
                    const hornMat = new THREE.MeshStandardMaterial({ color: 0xc98742, metalness: 0.55, roughness: 0.28 });
                    const eyeMat = new THREE.MeshBasicMaterial({ color: 0xffff55 });
                    const fireMat = new THREE.MeshBasicMaterial({ color: 0xff6a00 });

                    const body = new THREE.Mesh(new THREE.SphereGeometry(3.0, 20, 14), skinMat);
                    body.position.set(0, 4.0, 0);
                    body.scale.set(1.15, 1.0, 1.55);
                    group.add(body);

                    const chest = new THREE.Mesh(new THREE.SphereGeometry(2.15, 16, 12), scaleMat);
                    chest.position.set(0, 4.15, -1.65);
                    chest.scale.set(1.0, 1.05, 0.75);
                    group.add(chest);

                    const neck = new THREE.Mesh(new THREE.CylinderGeometry(1.05, 1.65, 3.4, 10), skinMat);
                    neck.position.set(0, 6.25, -0.95);
                    neck.rotation.x = -0.15;
                    group.add(neck);

                    const head = new THREE.Mesh(new THREE.SphereGeometry(1.75, 16, 12), skinMat);
                    head.position.set(0, 8.0, -1.75);
                    head.scale.set(1.18, 0.88, 1.35);
                    group.add(head);

                    // 아래턱을 따로 만들어 용 머리 실루엣 강화
                    const jaw = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.55, 2.25), scaleMat);
                    jaw.position.set(0, 7.45, -2.55);
                    jaw.rotation.x = -0.08;
                    group.add(jaw);

                    // 코/콧구멍
                    const nose = new THREE.Mesh(new THREE.ConeGeometry(0.62, 1.4, 8), scaleMat);
                    nose.rotation.x = -Math.PI / 2;
                    nose.position.set(0, 7.85, -3.05);
                    group.add(nose);

                    // 눈 + 눈썹 능선
                    [-1, 1].forEach(side => {
                        const eye = new THREE.Mesh(new THREE.SphereGeometry(0.2, 8, 8), eyeMat);
                        eye.position.set(side * 0.72, 8.18, -3.0);
                        group.add(eye);
                        const brow = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.22, 0.45), skinMat);
                        brow.position.set(side * 0.7, 8.48, -2.82);
                        brow.rotation.z = side * -0.22;
                        group.add(brow);
                    });

                    // 큰 뒤쪽 뿔 4개
                    [-1, 1].forEach(side => {
                        for (let k = 0; k < 2; k++) {
                            const horn = new THREE.Mesh(new THREE.ConeGeometry(0.32 - k * 0.06, 2.2 - k * 0.25, 8), hornMat);
                            horn.position.set(side * (0.8 + k * 0.38), 9.0 - k * 0.15, -1.2 + k * 0.15);
                            horn.rotation.z = side * (0.32 + k * 0.1);
                            horn.rotation.x = -0.25;
                            group.add(horn);
                        }
                    });

                    // 거대한 박쥐형 날개: 중앙 막 + 날개 뼈
                    [-1, 1].forEach(side => {
                        const membrane = new THREE.Mesh(new THREE.ConeGeometry(4.6, 7.2, 4, 1, true), wingMat);
                        membrane.position.set(side * 3.5, 6.0, 0.4);
                        membrane.rotation.z = side * (Math.PI / 2.15);
                        membrane.rotation.x = side * 0.08;
                        membrane.scale.set(1.0, 1.0, 0.55);
                        group.add(membrane);

                        for (let k = 0; k < 3; k++) {
                            const bone = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.14, 4.2, 6), hornMat);
                            bone.position.set(side * (3.0 + k * 0.9), 6.0 + k * 0.65, 0.2 + k * 0.25);
                            bone.rotation.z = side * (Math.PI / 2.3 - k * 0.12);
                            group.add(bone);
                        }
                    });

                    // 네 발 + 발톱
                    [-1, 1].forEach(side => {
                        [-1, 1].forEach(front => {
                            const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.62, 2.5, 8), skinMat);
                            leg.position.set(side * 1.55, 2.35, front * 1.0);
                            leg.rotation.z = side * 0.18;
                            group.add(leg);
                            for (let c = -1; c <= 1; c++) {
                                const claw = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.7, 6), hornMat);
                                claw.position.set(side * (1.55 + c * 0.28), 1.15, front * 1.25 + c * 0.12);
                                claw.rotation.x = front * 0.65;
                                group.add(claw);
                            }
                        });
                    });

                    // 긴 꼬리 + 꼬리 끝 가시
                    for (let i = 0; i < 7; i++) {
                        const r = 1.25 - i * 0.14;
                        const tail = new THREE.Mesh(new THREE.SphereGeometry(Math.max(r, 0.25), 10, 8), skinMat);
                        tail.position.set(0, 3.6 - i * 0.22, 2.0 + i * 1.35);
                        tail.scale.set(1.0, 0.85, 1.2);
                        group.add(tail);
                        if (i > 1) {
                            const spike = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.9, 6), hornMat);
                            spike.position.set(0, 4.0 - i * 0.2, 2.25 + i * 1.35);
                            spike.rotation.x = Math.PI / 2;
                            group.add(spike);
                        }
                    }

                    // 등가시
                    for (let i = 0; i < 5; i++) {
                        const spike = new THREE.Mesh(new THREE.ConeGeometry(0.32, 1.5, 6), hornMat);
                        spike.position.set(0, 6.2 - i * 0.55, 1.0 + i * 0.45);
                        spike.rotation.x = Math.PI / 2;
                        group.add(spike);
                    }

                    const core = new THREE.Mesh(new THREE.SphereGeometry(0.65, 12, 12), fireMat);
                    core.position.set(0, 4.5, -2.55);
                    group.add(core);
                    group.add(new THREE.PointLight(0xff3b00, 8, 30));

                    group.position.set(x, 0, z);
                    scene.add(group);

                    const maxHp = 950 + round * 300;
                    bossEnemy = { mesh: group, hp: maxHp, maxHp, speed: 3.4, damage: 18, lastAttack: 0,
                        lastSlam: performance.now(), isSlamming: false, slamPhase: 0, isBoss: true,
                        attackIndex: 0, lastBossAttack: performance.now(), attackCooldown: 4200 };
                    enemies.push(bossEnemy);
                }

                // 용이 입에서 플레이어 방향으로 길고 곧은 불줄기를 지속적으로 뿜음
                function createFireBreath(boss) {
                    const origin = boss.mesh.position.clone().add(new THREE.Vector3(0, 7.8, -4.0));
                    const target = camera.position.clone();
                    const dir = new THREE.Vector3().subVectors(target, origin).normalize();
                    const length = 28;
                    const center = origin.clone().add(dir.clone().multiplyScalar(length / 2));

                    const outer = new THREE.Mesh(
                        new THREE.CylinderGeometry(1.8, 0.8, length, 20, 1, true),
                        new THREE.MeshBasicMaterial({ color: 0xff2400, transparent: true, opacity: 0.55, side: THREE.DoubleSide })
                    );
                    outer.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
                    outer.position.copy(center);
                    scene.add(outer);

                    const inner = new THREE.Mesh(
                        new THREE.CylinderGeometry(0.72, 0.28, length * 0.98, 16, 1, true),
                        new THREE.MeshBasicMaterial({ color: 0xffd21f, transparent: true, opacity: 0.9, side: THREE.DoubleSide })
                    );
                    inner.quaternion.copy(outer.quaternion);
                    inner.position.copy(center);
                    scene.add(inner);

                    const flameParticles = [];
                    for (let i = 0; i < 24; i++) {
                        const t = Math.random();
                        const p = origin.clone().add(dir.clone().multiplyScalar(length * t));
                        const spread = 0.25 + t * 1.0;
                        p.x += (Math.random() - 0.5) * spread;
                        p.y += (Math.random() - 0.5) * spread;
                        p.z += (Math.random() - 0.5) * spread;
                        const f = new THREE.Mesh(new THREE.SphereGeometry(0.18 + Math.random() * 0.28, 7, 7),
                            new THREE.MeshBasicMaterial({ color: Math.random() > 0.4 ? 0xff4500 : 0xffd21f, transparent: true, opacity: 0.9 }));
                        f.position.copy(p);
                        scene.add(f);
                        flameParticles.push({ mesh: f, t, phase: Math.random() * Math.PI * 2 });
                    }

                    const start = performance.now();
                    const duration = 1800;
                    function animateBreath(now) {
                        const elapsed = now - start;
                        if (elapsed >= duration) {
                            scene.remove(outer); scene.remove(inner);
                            flameParticles.forEach(p => scene.remove(p.mesh));
                            return;
                        }
                        outer.scale.x = 1 + Math.sin(now * 0.018) * 0.08;
                        inner.scale.x = 1 + Math.sin(now * 0.025 + 1) * 0.12;
                        flameParticles.forEach(p => {
                            const wobble = Math.sin(now * 0.02 + p.phase) * (0.15 + p.t * 0.6);
                            p.mesh.position.x += wobble * 0.01;
                            p.mesh.position.y += Math.cos(now * 0.018 + p.phase) * 0.008;
                        });
                        requestAnimationFrame(animateBreath);
                    }
                    requestAnimationFrame(animateBreath);

                    // 불줄기 중심축에 가까우면 지속시간 동안 1회 피해
                    const toPlayer = new THREE.Vector3().subVectors(camera.position, origin);
                    const along = toPlayer.dot(dir);
                    const perpendicular = toPlayer.clone().sub(dir.clone().multiplyScalar(along)).length();
                    if (along > 0 && along < length && perpendicular < 2.0) {
                        playerHealth -= 32;
                        updateHUD();
                        if (playerHealth <= 0) endGame(false);
                    }
                }

                

function createShockwave(x, z) {
                    const geo = new THREE.RingGeometry(0.5, 1.5, 32);
                    const mat = new THREE.MeshBasicMaterial({ color: 0xff0055, side: THREE.DoubleSide, transparent: true, opacity: 0.9 });
                    const ring = new THREE.Mesh(geo, mat);
                    ring.rotation.x = Math.PI / 2;
                    ring.position.set(x, 0.1, z);
                    scene.add(ring);

                    shockwaves.push({
                        mesh: ring,
                        radius: 1.5,
                        maxRadius: 18.0,
                        speed: 22.0,
                        originX: x,
                        originZ: z,
                        hasHitPlayer: false
                    });

                    playGunSound('slam');
                }

                function onKeyDown(e) {
                    initAudio();
                    if (!isGameActive) return;
                    if (e.code === 'KeyB') { toggleShop(); return; }
                    if (e.code === 'KeyO') { toggleFullScreen(); return; }
                    if (e.code === 'KeyM') { skipRound(); return; } // M 키 누를 시 라운드 스킵
                    if (isShopOpen) return;

                    switch (e.code) {
                        case 'KeyW': moveForward = true; break;
                        case 'KeyS': moveBackward = true; break;
                        case 'KeyA': moveLeft = true; break;
                        case 'KeyD': moveRight = true; break;
                        case 'ShiftLeft': isSprinting = true; break;
                        case 'Space': 
                            if (isGrounded) {
                                playerVelocityY = JUMP_FORCE;
                                isGrounded = false;
                            }
                            break;
                        case 'KeyR': reload(); break;
                        case 'KeyE': shoot(); break;
                        case 'Digit1': switchWeapon(1); break;
                        case 'Digit2': switchWeapon(2); break;
                        case 'Digit3': if (WEAPONS[3].owned) switchWeapon(3); break;
                        case 'Digit4': if (WEAPONS[4].owned) switchWeapon(4); break;
                    }
                }

                function onKeyUp(e) {
                    switch (e.code) {
                        case 'KeyW': moveForward = false; break;
                        case 'KeyS': moveBackward = false; break;
                        case 'KeyA': moveLeft = false; break;
                        case 'KeyD': moveRight = false; break;
                        case 'ShiftLeft': isSprinting = false; break;
                    }
                }

                function switchWeapon(id) {
                    if (isReloading || currentWeaponId === id) return;
                    currentWeaponId = id;
                    currentAmmo = WEAPONS[id].magSize;
                    createGunModel();
                    updateHUD();
                }

                function reload() {
                    const w = WEAPONS[currentWeaponId];
                    if (isReloading || currentAmmo === w.magSize) return;
                    isReloading = true;
                    document.getElementById('weapon').innerText = `${w.name} (재장전 중...)`;
                    setTimeout(() => {
                        currentAmmo = w.magSize;
                        isReloading = false;
                        updateHUD();
                    }, w.reloadTime);
                }

                function triggerMuzzleEffect() {
                    const flash = document.getElementById('muzzle-flash-hud');
                    flash.style.display = 'block';
                    setTimeout(() => { flash.style.display = 'none'; }, 40);

                    if (gunMesh) {
                        const gunWorldPos = new THREE.Vector3();
                        gunMesh.getWorldPosition(gunWorldPos);
                        muzzleLight.position.copy(gunWorldPos);
                        muzzleLight.intensity = 5;
                        setTimeout(() => { muzzleLight.intensity = 0; }, 50);
                    }
                }

                function shoot() {
                    const now = performance.now();
                    const w = WEAPONS[currentWeaponId];
                    if (now - lastShotTime < w.fireRate) return;
                    if (currentAmmo <= 0) { reload(); return; }

                    lastShotTime = now;
                    currentAmmo--;
                    
                    playGunSound(currentWeaponId);
                    triggerMuzzleEffect();
                    updateHUD();

                    if (gunMesh) {
                        gunMesh.position.z += 0.08;
                        setTimeout(() => { if (gunMesh) gunMesh.position.z -= 0.08; }, 40);
                    }

                    pitch += w.recoil;

                    const raycaster = new THREE.Raycaster();
                    const count = w.pellets || 1;

                    for (let i = 0; i < count; i++) {
                        const spreadX = (Math.random() - 0.5) * (w.recoil * 1.5);
                        const spreadY = (Math.random() - 0.5) * (w.recoil * 1.5);
                        raycaster.setFromCamera(new THREE.Vector2(spreadX, spreadY), camera);
                        
                        const enemyMeshes = enemies.flatMap(e => e.mesh.children);
                        const intersects = raycaster.intersectObjects(enemyMeshes);

                        if (intersects.length > 0 && intersects[0].distance <= w.range) {
                            const hitMesh = intersects[0].object;
                            const enemyObj = enemies.find(e => e.mesh.children.includes(hitMesh));
                            if (enemyObj) {
                                enemyObj.hp -= w.damage;
                                updateHUD();
                                if (enemyObj.hp <= 0) {
                                    scene.remove(enemyObj.mesh);
                                    enemies = enemies.filter(e => e !== enemyObj);
                                    kills++;
                                    money += enemyObj.isBoss ? 500 : 25;
                                    if (enemyObj.isBoss) bossEnemy = null;
                                    updateHUD();
                                    if (enemies.length === 0) endGame(true);
                                }
                            }
                        }
                    }
                }

                function updateHUD() {
                    document.getElementById('round').innerText = round;
                    document.getElementById('health').innerText = Math.max(0, Math.round(playerHealth));
                    document.getElementById('money').innerText = money;
                    document.getElementById('weapon').innerText = WEAPONS[currentWeaponId].name;
                    document.getElementById('ammo').innerText = `${currentAmmo} / ${WEAPONS[currentWeaponId].magSize}`;
                    document.getElementById('kills').innerText = kills;
                    document.getElementById('enemies-left').innerText = enemies.length;

                    if (bossEnemy) {
                        const bossPct = Math.max(0, (bossEnemy.hp / bossEnemy.maxHp) * 100);
                        document.getElementById('boss-hp-fill').style.width = `${bossPct}%`;
                    }

                    const healthElem = document.getElementById('health');
                    if (playerHealth < 30) healthElem.style.color = '#ff3333';
                    else if (playerHealth < 60) healthElem.style.color = '#ffaa00';
                    else healthElem.style.color = '#00ffcc';
                }

                function endGame(victory) {
                    isGameActive = false;
                    isRoundCleared = victory;
                    gameOverScreen.style.display = 'block';

                    const title = document.getElementById('game-over-title');
                    const desc = document.getElementById('game-over-desc');
                    const btn = document.getElementById('game-over-btn');

                    if (victory) {
                        if (!roundRewardGiven) {
                            money += 100;
                            roundRewardGiven = true;
                            updateHUD();
                        }
                        title.innerText = `라운드 ${round} 승리!`;
                        title.style.color = '#00ffcc';
                        desc.innerText = round % 5 === 0 ? '보스를 물리쳤습니다!' : '적을 모두 제압했습니다!';
                        btn.innerText = '다음 라운드 진입';
                    } else {
                        title.innerText = '패배했습니다...';
                        title.style.color = '#ff3333';
                        desc.innerText = `적에게 제압당했습니다. (최종 라운드: ${round})`;
                        btn.innerText = '다시 시작하기';
                    }
                }

                function resetOrNextRound() {
                    gameOverScreen.style.display = 'none';
                    if (isRoundCleared) {
                        round++;
                    } else {
                        round = 1;
                        kills = 0;
                        money = 0;
                        WEAPONS[3].owned = false;
                        WEAPONS[4].owned = false;
                        currentWeaponId = 1;
                        createGunModel();
                    }
                    startRound();
                    isGameActive = true;
                }

                function animate() {
                    requestAnimationFrame(animate);
                    const time = performance.now();
                    const delta = (time - prevTime) / 1000;
                    prevTime = time;

                    if (isGameActive && !isShopOpen) {
                        // 기관총은 좌클릭을 누르고 있는 동안 자동 연사
                        if (isMouseDown && currentWeaponId === 4 && !isReloading) shoot();

                        playerVelocityY += GRAVITY * delta;
                        camera.position.y += playerVelocityY * delta;

                        if (camera.position.y <= PLAYER_HEIGHT) {
                            camera.position.y = PLAYER_HEIGHT;
                            playerVelocityY = 0;
                            isGrounded = true;
                        }

                        velocity.x -= velocity.x * 10.0 * delta;
                        velocity.z -= velocity.z * 10.0 * delta;

                        direction.z = Number(moveForward) - Number(moveBackward);
                        direction.x = Number(moveRight) - Number(moveLeft);
                        direction.normalize();

                        const moveSpeed = isSprinting ? 65.0 : 35.0;
                        if (moveForward || moveBackward) velocity.z -= direction.z * moveSpeed * delta;
                        if (moveLeft || moveRight) velocity.x -= direction.x * moveSpeed * delta;

                        camera.translateX(-velocity.x * delta);
                        camera.translateZ(velocity.z * delta);

                        const playerPos = camera.position;

                        enemies.forEach(enemy => {
                            const enemyPos = enemy.mesh.position;

                            if (enemy.isBoss) {
                                // 보스 공격 순서: 파동 -> 파동 -> 불 브레스 -> 반복
                                if (!enemy.isSlamming && time - enemy.lastBossAttack > enemy.attackCooldown) {
                                    if (enemy.attackIndex === 2) {
                                        createFireBreath(enemy);
                                        enemy.attackIndex = 0;
                                    } else {
                                        enemy.isSlamming = true;
                                        enemy.slamPhase = 1;
                                        enemy.lastSlam = time;
                                        enemy.attackIndex++;
                                    }
                                    enemy.lastBossAttack = time;
                                }

                                if (enemy.isSlamming) {
                                    if (enemy.slamPhase === 1) {
                                        enemyPos.y += 18 * delta;
                                        if (enemyPos.y >= 8.0) enemy.slamPhase = 2;
                                    } else if (enemy.slamPhase === 2) {
                                        enemyPos.y -= 40 * delta;
                                        if (enemyPos.y <= 0) {
                                            enemyPos.y = 0;
                                            enemy.isSlamming = false;
                                            createShockwave(enemyPos.x, enemyPos.z);
                                        }
                                    }
                                } else {
                                    const dist = enemyPos.distanceTo(playerPos);
                                    if (dist > 4.0) {
                                        const dir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                        enemyPos.x += dir.x * enemy.speed * delta;
                                        enemyPos.z += dir.z * enemy.speed * delta;
                                        enemy.mesh.lookAt(playerPos.x, enemyPos.y, playerPos.z);
                                    } else if (time - enemy.lastAttack > 1000) {
                                        playerHealth -= enemy.damage;
                                        enemy.lastAttack = time;
                                        updateHUD();
                                        if (playerHealth <= 0) endGame(false);
                                    }
                                }
                            } else {
                                const dist = enemyPos.distanceTo(playerPos);
                                if (dist > 1.8) {
                                    const dir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                    enemyPos.x += dir.x * enemy.speed * delta;
                                    enemyPos.z += dir.z * enemy.speed * delta;
                                    enemy.mesh.lookAt(playerPos.x, enemyPos.y, playerPos.z);
                                } else {
                                    if (time - enemy.lastAttack > 1000) {
                                        playerHealth -= enemy.damage;
                                        enemy.lastAttack = time;
                                        updateHUD();
                                        if (playerHealth <= 0) endGame(false);
                                    }
                                }
                            }
                        });

                        for (let i = shockwaves.length - 1; i >= 0; i--) {
                            const wave = shockwaves[i];
                            wave.radius += wave.speed * delta;
                            wave.mesh.scale.set(wave.radius, wave.radius, 1);
                            wave.mesh.material.opacity = 1 - (wave.radius / wave.maxRadius);

                            const distToPlayer = Math.hypot(playerPos.x - wave.originX, playerPos.z - wave.originZ);
                            if (!wave.hasHitPlayer && Math.abs(distToPlayer - wave.radius) < 1.8) {
                                if (camera.position.y < PLAYER_HEIGHT + 1.2) {
                                    playerHealth -= 35;
                                    wave.hasHitPlayer = true;
                                    updateHUD();
                                    if (playerHealth <= 0) endGame(false);
                                }
                            }

                            if (wave.radius >= wave.maxRadius) {
                                scene.remove(wave.mesh);
                                shockwaves.splice(i, 1);
                            }
                        }
                    }
                    renderer.render(scene, camera);
                }

                window.onload = init;
            </script>
        </body>
        </html>
        """
        
        components.html(game_html, height=800)

if __name__ == "__main__":
    main()
