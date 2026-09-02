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
        **패치 내역:**
        - **드래곤 보스 강화**: 체력 증가(1600), 브레스 지속시간 및 범위 대폭 확대, 충격파 범위 증가
        - **디테일한 3D 모델링**: 드래곤(얼굴, 눈, 꼬리, 날개) & 소드마스터(투구, 팔, 다리, 정교한 검)
        - **M 키 치트**: 라운드 스킵 & +100 Gold 지급
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
                    background: linear-gradient(90deg, #00f0ff, #ff0055);
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
                    min-width: 380px;
                    max-height: 80vh;
                    overflow-y: auto;
                    text-align: center;
                    cursor: default;
                }
                .buy-item {
                    margin: 10px 0;
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
                    라운드: <span id="round">1</span> / 10 | 
                    체력: <span id="health" style="color: #00ffcc;">150</span> | 
                    골드: <span id="money" style="color:#ffd700;">0</span>G | 
                    무기: <span id="weapon">권총</span> | 
                    탄약: <span id="ammo">12 / 12</span> | 
                    처치: <span id="kills">0</span> | 
                    남은 적: <span id="enemies-left">0</span>
                </div>

                <div id="boss-hud">
                    ⚠️ 보스 : <span id="boss-title">소드마스터</span>
                    <div id="boss-hp-bar"><div id="boss-hp-fill"></div></div>
                </div>

                <div id="crosshair"></div>
                
                <div id="top-controls">
                    <button id="shop-btn" class="ui-btn" onclick="toggleShop()">🛒 상점 (B)</button>
                    <button id="fullscreen-btn" class="ui-btn" onclick="toggleFullScreen()">🖥️ 전체 화면 (O)</button>
                </div>

                <div id="shop-modal">
                    <h2 style="color: #ffd700; margin-top:0;">상점 & 무기 연구소</h2>
                    <p>보유 골드: <span id="shop-money" style="color: #ffd700; font-weight: bold;">0</span>G</p>
                    <hr style="border-color: #444;">
                    
                    <div class="buy-item">
                        <h4 style="margin: 0; color: #00ff88;">🧪 체력 포션 (Potion) - [H]</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">체력을 20 회복합니다.</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 50G</p>
                        <button id="buy-potion-btn" class="buy-btn" onclick="buyPotion()">체력 포션 구매 (50G)</button>
                    </div>

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

                    <div class="buy-item">
                        <h4 style="margin: 0; color: #ff3300;">🚀 바주카포 (Bazooka)</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">강력한 폭발 화력! | 탄창: 1발</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 600G</p>
                        <button id="buy-bazooka-btn" class="buy-btn" onclick="buyWeapon(5)">바주카포 구매 (600G)</button>
                    </div>

                    <div class="buy-item">
                        <h4 style="margin: 0; color: #00f0ff;">⚡ 레이저총 (Laser Cannon) - [L]</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">관통 레이저 사격 | 탄창: 15발</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 1,200G</p>
                        <button id="buy-laser-btn" class="buy-btn" onclick="buyWeapon(6)">레이저총 구매 (1200G)</button>
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
                    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                    if (audioCtx.state === 'suspended') audioCtx.resume();
                }

                function playSound(type) {
                    initAudio();
                    if (!audioCtx) return;

                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    
                    if (type === 'shot') {
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(320, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.08);
                        gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
                    } else if (type === 'laser') {
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(900, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.2);
                        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                    } else if (type === 'sword_wave') {
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(600, audioCtx.currentTime);
                        osc.frequency.linearRampToValueAtTime(200, audioCtx.currentTime + 0.25);
                        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
                    } else if (type === 'charge') {
                        osc.type = 'triangle';
                        osc.frequency.setValueAtTime(100, audioCtx.currentTime);
                        osc.frequency.linearRampToValueAtTime(500, audioCtx.currentTime + 0.8);
                        gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.8);
                    } else if (type === 'dash') {
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(200, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(50, audioCtx.currentTime + 0.3);
                        gain.gain.setValueAtTime(0.6, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                    } else if (type === 'slam' || type === 'explosion') {
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(150, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.5);
                        gain.gain.setValueAtTime(0.8, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                    } else if (type === 'breath') {
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(90, audioCtx.currentTime);
                        osc.frequency.linearRampToValueAtTime(180, audioCtx.currentTime + 0.6);
                        gain.gain.setValueAtTime(0.6, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.6);
                    }
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.9);
                }

                const WEAPONS = {
                    1: { name: '권총', damage: 30, range: 45, fireRate: 250, magSize: 12, reloadTime: 1000, color: 0x00ffcc, owned: true },
                    2: { name: '소총', damage: 60, range: 65, fireRate: 110, magSize: 30, reloadTime: 1800, color: 0x3388ff, owned: true },
                    3: { name: '산탄총', damage: 22, range: 20, fireRate: 650, magSize: 6, reloadTime: 2200, color: 0xff8800, owned: false, price: 150 },
                    4: { name: '기관총', damage: 12, range: 75, fireRate: 75, magSize: 100, reloadTime: 2800, color: 0xffd700, owned: false, price: 300 },
                    5: { name: '바주카포', damage: 220, range: 110, fireRate: 1400, magSize: 1, reloadTime: 2200, color: 0xff2200, owned: false, price: 600 },
                    6: { name: '레이저총', damage: 65, range: 130, fireRate: 130, magSize: 15, reloadTime: 1600, color: 0x00f0ff, owned: false, price: 1200 }
                };

                let round = 1, kills = 0, money = 0, playerHealth = 150, maxPlayerHealth = 150;
                let isMouseDown = false;
                let currentWeaponId = 1, currentAmmo = WEAPONS[1].magSize;
                let isReloading = false, lastShotTime = 0;

                let scene, camera, renderer, gunMesh, muzzlePoint, muzzleFlashLight;
                let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false, isSprinting = false;
                
                let playerVelocityY = 0;
                let isGrounded = true;
                const GRAVITY = -28.0;
                const JUMP_FORCE = 10.5;
                const PLAYER_HEIGHT = 1.6;

                let prevTime = performance.now();
                let velocity = new THREE.Vector3(), direction = new THREE.Vector3();
                let enemies = [], shockwaves = [], swordWaves = [], breathParticles = [], explosionEffects = [], visualEffects = [];
                let isGameActive = false, isShopOpen = false;
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

                    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
                    scene.add(ambientLight);

                    const dirLight = new THREE.DirectionalLight(0x00ffcc, 0.8);
                    dirLight.position.set(20, 40, 20);
                    scene.add(dirLight);

                    renderer = new THREE.WebGLRenderer({ antialias: true });
                    renderer.setSize(window.innerWidth, window.innerHeight);
                    document.getElementById('game-container').appendChild(renderer.domElement);

                    createGunModel();

                    const container = document.getElementById('game-container');
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
                    container.addEventListener('mouseup', (e) => { if (e.button === 0) isMouseDown = false; });
                    container.addEventListener('mouseleave', () => { isMouseDown = false; });

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
                        container.requestFullscreen().catch(err => alert(`전체 화면 전환 실패: ${err.message}`));
                    } else {
                        document.exitFullscreen();
                    }
                }

                function createGunModel() {
                    if (gunMesh) camera.remove(gunMesh);

                    const gunGroup = new THREE.Group();
                    const w = WEAPONS[currentWeaponId];
                    
                    let bodyGeo, gunLength = 0.5;
                    if (currentWeaponId === 1) { bodyGeo = new THREE.BoxGeometry(0.08, 0.12, 0.35); gunLength = 0.35; }
                    else if (currentWeaponId === 2) { bodyGeo = new THREE.BoxGeometry(0.1, 0.14, 0.65); gunLength = 0.65; }
                    else if (currentWeaponId === 3) { bodyGeo = new THREE.BoxGeometry(0.14, 0.16, 0.7); gunLength = 0.7; }
                    else if (currentWeaponId === 4) { bodyGeo = new THREE.BoxGeometry(0.18, 0.2, 0.85); gunLength = 0.85; }
                    else if (currentWeaponId === 5) { bodyGeo = new THREE.CylinderGeometry(0.1, 0.1, 0.9, 12); gunLength = 0.9; }
                    else { bodyGeo = new THREE.BoxGeometry(0.12, 0.15, 0.75); gunLength = 0.75; }

                    const bodyMat = new THREE.MeshStandardMaterial({ color: w.color, metalness: 0.8, roughness: 0.2 });
                    const body = new THREE.Mesh(bodyGeo, bodyMat);
                    if (currentWeaponId === 5) body.rotation.x = Math.PI / 2;
                    body.position.set(0.25, -0.2, -0.4);
                    gunGroup.add(body);

                    muzzlePoint = new THREE.Object3D();
                    muzzlePoint.position.set(0.25, -0.2, -0.4 - (gunLength / 2));
                    gunGroup.add(muzzlePoint);

                    muzzleFlashLight = new THREE.PointLight(w.color, 0, 5);
                    muzzlePoint.add(muzzleFlashLight);

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
                    document.getElementById('shop-modal').style.display = isShopOpen ? 'block' : 'none';
                    document.getElementById('shop-money').innerText = money;
                }

                function buyPotion() {
                    if (money >= 50 && playerHealth < maxPlayerHealth) {
                        money -= 50;
                        playerHealth = Math.min(maxPlayerHealth, playerHealth + 20);
                        updateHUD();
                        toggleShop();
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

                function buildMap() {
                    const gridHelper = new THREE.GridHelper(100, 50, 0x00ffcc, 0x333355);
                    gridHelper.position.y = 0.01;
                    scene.add(gridHelper);

                    const floorGeo = new THREE.PlaneGeometry(100, 100);
                    const floorMat = new THREE.MeshStandardMaterial({ color: 0x0a0a18, roughness: 0.5 });
                    const floor = new THREE.Mesh(floorGeo, floorMat);
                    floor.rotation.x = -Math.PI / 2;
                    scene.add(floor);
                }

                function startRound() {
                    enemies.forEach(e => scene.remove(e.mesh));
                    enemies = [];
                    bossEnemy = null;
                    
                    shockwaves.forEach(s => scene.remove(s.mesh));
                    shockwaves = [];
                    swordWaves.forEach(sw => scene.remove(sw.mesh));
                    swordWaves = [];
                    breathParticles.forEach(b => scene.remove(b.mesh));
                    breathParticles = [];
                    explosionEffects.forEach(ex => scene.remove(ex.mesh));
                    explosionEffects = [];
                    visualEffects.forEach(ve => scene.remove(ve.mesh));
                    visualEffects = [];

                    playerHealth = 150;
                    roundRewardGiven = false;
                    camera.position.set(0, PLAYER_HEIGHT, 40);
                    
                    document.getElementById('boss-hud').style.display = 'none';

                    if (round === 5) {
                        createBossEnemy(0, -20);
                        document.getElementById('boss-hud').style.display = 'block';
                        document.getElementById('boss-title').innerText = "크로노스 드래곤";
                    } else if (round === 10) {
                        createSwordBossEnemy(0, -20);
                        document.getElementById('boss-hud').style.display = 'block';
                        document.getElementById('boss-title').innerText = "소드마스터";
                    } else {
                        const enemyCount = round * 2 + 2;
                        for (let i = 0; i < enemyCount; i++) {
                            createEnemy((Math.random()-0.5)*40, (Math.random()-0.5)*40 - 10);
                        }
                    }
                    updateHUD();
                }

                function createEnemy(x, z) {
                    const group = new THREE.Group();
                    const body = new THREE.Mesh(new THREE.ConeGeometry(0.8, 1.4, 6), new THREE.MeshStandardMaterial({ color: 0xaa2255 }));
                    body.rotation.x = Math.PI;
                    body.position.y = 1.3;
                    group.add(body);

                    group.position.set(x, 0, z);
                    scene.add(group);

                    enemies.push({
                        mesh: group,
                        hp: 60 + (round * 12),
                        maxHp: 60 + (round * 12),
                        speed: 5.5 + (Math.random() * 2.0),
                        damage: 12,
                        lastAttack: 0,
                        isBoss: false
                    });
                }

                // 디테일한 드래곤 보스 생성 (얼굴, 눈, 입, 대형 날개, 가시 꼬리)
                function createBossEnemy(x, z) {
                    const group = new THREE.Group();
                    const skinMat = new THREE.MeshStandardMaterial({ color: 0x991122, metalness: 0.5, roughness: 0.3 });
                    const eyeMat = new THREE.MeshBasicMaterial({ color: 0xffea00 });
                    const wingMat = new THREE.MeshStandardMaterial({ color: 0xbb1100, side: THREE.DoubleSide });

                    // 몸통
                    const body = new THREE.Mesh(new THREE.ConeGeometry(2.5, 6.5, 8), skinMat);
                    body.rotation.x = Math.PI / 2;
                    body.position.set(0, 3.8, 0);
                    group.add(body);

                    // 머리 및 입
                    const headGroup = new THREE.Group();
                    headGroup.position.set(0, 4.8, -3.2);

                    const headBox = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.4, 2.2), skinMat);
                    headGroup.add(headBox);

                    const snout = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.9, 1.5), skinMat);
                    snout.position.set(0, -0.2, -1.4);
                    headGroup.add(snout);

                    // 양쪽 눈
                    const leftEye = new THREE.Mesh(new THREE.SphereGeometry(0.2, 8, 8), eyeMat);
                    leftEye.position.set(-0.7, 0.3, -0.6);
                    const rightEye = leftEye.clone();
                    rightEye.position.x = 0.7;
                    headGroup.add(leftEye);
                    headGroup.add(rightEye);

                    group.add(headGroup);

                    // 대형 3D 날개
                    const leftWing = new THREE.Mesh(new THREE.BoxGeometry(7.0, 0.1, 3.0), wingMat);
                    leftWing.position.set(-4.2, 4.5, 0.5);
                    leftWing.rotation.z = Math.PI / 12;
                    leftWing.rotation.y = -Math.PI / 12;

                    const rightWing = leftWing.clone();
                    rightWing.position.x = 4.2;
                    rightWing.rotation.z = -Math.PI / 12;
                    rightWing.rotation.y = Math.PI / 12;

                    group.add(leftWing);
                    group.add(rightWing);

                    // 가시 꼬리
                    const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 1.2, 6.0, 8), skinMat);
                    tail.rotation.x = Math.PI / 3;
                    tail.position.set(0, 2.2, 4.0);
                    group.add(tail);

                    group.position.set(x, 0, z);
                    scene.add(group);

                    const maxHp = 1600; // 체력 상향
                    bossEnemy = {
                        mesh: group,
                        hp: maxHp,
                        maxHp: maxHp,
                        speed: 5.0,
                        isBoss: true,
                        bossType: 'dragon',
                        state: 'walk',
                        jumpVelocityY: 0,
                        lastSkillTime: performance.now(),
                        skillCooldown: 3200
                    };
                    enemies.push(bossEnemy);
                }

                // 디테일한 소드마스터 생성 (머리, 투구, 눈, 양 팔, 양 다리, 거대 레이저 검)
                function createSwordBossEnemy(x, z) {
                    const group = new THREE.Group();
                    const armorMat = new THREE.MeshStandardMaterial({ color: 0x151522, metalness: 0.9, roughness: 0.2 });
                    const eyeMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff });
                    const swordMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, emissive: 0x00f0ff, emissiveIntensity: 0.9 });

                    // 몸통
                    const torso = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.4, 1.0), armorMat);
                    torso.position.y = 2.6;
                    group.add(torso);

                    // 머리 (투구 및 빛나는 눈)
                    const head = new THREE.Mesh(new THREE.BoxGeometry(1.0, 1.0, 1.0), armorMat);
                    head.position.y = 4.2;
                    
                    const visior = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.2, 0.2), eyeMat);
                    visior.position.set(0, 0.1, -0.5);
                    head.add(visior);
                    group.add(head);

                    // 양 팔
                    const armGeo = new THREE.BoxGeometry(0.5, 2.0, 0.5);
                    const leftArm = new THREE.Mesh(armGeo, armorMat);
                    leftArm.position.set(-1.2, 2.6, 0);

                    const rightArm = new THREE.Mesh(armGeo, armorMat);
                    rightArm.position.set(1.2, 2.6, 0);
                    group.add(leftArm);
                    group.add(rightArm);

                    // 양 다리
                    const legGeo = new THREE.BoxGeometry(0.6, 2.2, 0.6);
                    const leftLeg = new THREE.Mesh(legGeo, armorMat);
                    leftLeg.position.set(-0.5, 1.1, 0);

                    const rightLeg = new THREE.Mesh(legGeo, armorMat);
                    rightLeg.position.set(0.5, 1.1, 0);
                    group.add(leftLeg);
                    group.add(rightLeg);

                    // 대형검
                    const swordGroup = new THREE.Group();
                    const blade = new THREE.Mesh(new THREE.BoxGeometry(0.3, 5.2, 0.6), swordMat);
                    blade.position.y = 2.6;
                    swordGroup.add(blade);

                    const hilt = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.3, 0.4), armorMat);
                    swordGroup.add(hilt);

                    swordGroup.position.set(1.4, 2.6, -0.4);
                    swordGroup.rotation.x = Math.PI / 4;
                    group.add(swordGroup);

                    // 기 모으기 아우라
                    const auraGeo = new THREE.SphereGeometry(2.8, 16, 16);
                    const auraMat = new THREE.MeshBasicMaterial({ color: 0xff0055, transparent: true, opacity: 0 });
                    const auraMesh = new THREE.Mesh(auraGeo, auraMat);
                    auraMesh.position.y = 2.6;
                    group.add(auraMesh);

                    group.position.set(x, 0, z);
                    scene.add(group);

                    const maxHp = 2800;
                    bossEnemy = {
                        mesh: group,
                        auraMesh: auraMesh,
                        hp: maxHp,
                        maxHp: maxHp,
                        speed: 5.5,
                        isBoss: true,
                        bossType: 'blade',
                        state: 'walk',
                        chargeTimer: 0,
                        dashDir: new THREE.Vector3(),
                        lastSkillTime: performance.now(),
                        skillCooldown: 3000,
                        lastSuperJumpTime: performance.now(),
                        superJumpCooldown: 12000,
                        targetLandPos: new THREE.Vector3()
                    };
                    enemies.push(bossEnemy);
                }

                function spawnSwordWave(bossPos, targetPos) {
                    playSound('sword_wave');
                    const waveGeo = new THREE.TorusGeometry(2.2, 0.2, 8, 24, Math.PI);
                    const waveMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, side: THREE.DoubleSide });
                    const waveMesh = new THREE.Mesh(waveGeo, waveMat);

                    const startPos = bossPos.clone().add(new THREE.Vector3(0, 2.6, 0));
                    waveMesh.position.copy(startPos);
                    waveMesh.lookAt(targetPos);
                    waveMesh.rotation.z += Math.PI / 2;

                    const dir = new THREE.Vector3().subVectors(targetPos, startPos).normalize();
                    scene.add(waveMesh);

                    swordWaves.push({ mesh: waveMesh, dir: dir, speed: 28.0, life: 3.0, damage: 30 });
                }

                function createShockwave(pos, radius, damage) {
                    const geo = new THREE.RingGeometry(0.5, radius, 32);
                    const mat = new THREE.MeshBasicMaterial({ color: 0xff0055, side: THREE.DoubleSide, transparent: true, opacity: 0.9 });
                    const ring = new THREE.Mesh(geo, mat);
                    ring.rotation.x = -Math.PI / 2;
                    ring.position.copy(pos);
                    ring.position.y = 0.1;

                    scene.add(ring);
                    shockwaves.push({ mesh: ring, maxRadius: radius, damage: damage, currentScale: 0.1, expandSpeed: 30.0 });
                    playSound('slam');
                }

                // 강화된 드래곤 브레스 발사 (연사 수량 45개, 오랫동안 지속 분사)
                function spawnDragonBreath(dragonPos, forwardDir) {
                    playSound('breath');
                    for (let i = 0; i < 45; i++) {
                        const pGeo = new THREE.SphereGeometry(0.4 + Math.random()*0.5, 8, 8);
                        const pMat = new THREE.MeshBasicMaterial({ color: Math.random() > 0.4 ? 0xff2200 : 0xffaa00, transparent: true, opacity: 0.85 });
                        const pMesh = new THREE.Mesh(pGeo, pMat);
                        
                        const startPos = dragonPos.clone().add(new THREE.Vector3(0, 4.5, -3.0));
                        pMesh.position.copy(startPos);
                        
                        const spreadDir = forwardDir.clone().add(new THREE.Vector3((Math.random()-0.5)*0.6, (Math.random()-0.5)*0.3, (Math.random()-0.5)*0.6)).normalize();
                        scene.add(pMesh);

                        breathParticles.push({
                            mesh: pMesh,
                            velocity: spreadDir.multiplyScalar(20.0 + Math.random()*14.0),
                            life: 2.2 // 오래 지속
                        });
                    }
                }

                function createExplosionEffect(pos) {
                    playSound('explosion');
                    const geo = new THREE.SphereGeometry(1.2, 16, 16);
                    const mat = new THREE.MeshBasicMaterial({ color: 0xff0033, transparent: true, opacity: 1.0 });
                    const mesh = new THREE.Mesh(geo, mat);
                    mesh.position.copy(pos);
                    mesh.position.y = 1.0;
                    scene.add(mesh);

                    explosionEffects.push({ mesh: mesh, scale: 1.0, opacity: 1.0 });
                }

                function onKeyDown(e) {
                    initAudio();
                    if (!isGameActive) return;
                    if (e.code === 'KeyM') { skipRoundWithCheat(); return; }
                    if (e.code === 'KeyB') { toggleShop(); return; }
                    if (e.code === 'KeyO') { toggleFullScreen(); return; }
                    if (e.code === 'KeyH') { buyPotion(); return; }
                    if (e.code === 'KeyL') { buyWeapon(6); return; }
                    if (isShopOpen) return;

                    switch (e.code) {
                        case 'KeyW': moveForward = true; break;
                        case 'KeyS': moveBackward = true; break;
                        case 'KeyA': moveLeft = true; break;
                        case 'KeyD': moveRight = true; break;
                        case 'ShiftLeft': isSprinting = true; break;
                        case 'Space': 
                            if (isGrounded) { playerVelocityY = JUMP_FORCE; isGrounded = false; }
                            break;
                        case 'KeyR': reload(); break;
                        case 'KeyE': shoot(); break;
                        case 'Digit1': switchWeapon(1); break;
                        case 'Digit2': switchWeapon(2); break;
                        case 'Digit3': if (WEAPONS[3].owned) switchWeapon(3); break;
                        case 'Digit4': if (WEAPONS[4].owned) switchWeapon(4); break;
                        case 'Digit5': if (WEAPONS[5].owned) switchWeapon(5); break;
                        case 'Digit6': if (WEAPONS[6].owned) switchWeapon(6); break;
                    }
                }

                function skipRoundWithCheat() {
                    money += 100;
                    if (round < 10) {
                        round++;
                        startRound();
                    } else {
                        endGame(true);
                    }
                    updateHUD();
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

                function triggerMuzzleEffect(targetPoint) {
                    const w = WEAPONS[currentWeaponId];
                    if (muzzleFlashLight) {
                        muzzleFlashLight.intensity = 4.0;
                        setTimeout(() => { if (muzzleFlashLight) muzzleFlashLight.intensity = 0; }, 50);
                    }

                    const startPos = new THREE.Vector3();
                    muzzlePoint.getWorldPosition(startPos);

                    if (currentWeaponId === 6) {
                        playSound('laser');
                        const dist = startPos.distanceTo(targetPoint);
                        const geom = new THREE.CylinderGeometry(0.05, 0.05, dist, 8);
                        geom.rotateX(Math.PI / 2);
                        const mat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.9 });
                        const laserMesh = new THREE.Mesh(geom, mat);
                        laserMesh.position.copy(startPos).add(targetPoint).multiplyScalar(0.5);
                        laserMesh.lookAt(targetPoint);
                        scene.add(laserMesh);
                        visualEffects.push({ mesh: laserMesh, life: 0.12 });
                    } else if (currentWeaponId === 5) {
                        playSound('bazooka');
                        createExplosionEffect(targetPoint);
                    } else {
                        const points = [startPos, targetPoint];
                        const geom = new THREE.BufferGeometry().setFromPoints(points);
                        const mat = new THREE.LineBasicMaterial({ color: w.color, transparent: true, opacity: 0.8 });
                        const line = new THREE.Line(geom, mat);
                        scene.add(line);
                        visualEffects.push({ mesh: line, life: 0.08 });
                    }
                }

                function shoot() {
                    const now = performance.now();
                    const w = WEAPONS[currentWeaponId];
                    if (now - lastShotTime < w.fireRate) return;
                    if (currentAmmo <= 0) { reload(); return; }

                    lastShotTime = now;
                    currentAmmo--;
                    
                    if (currentWeaponId !== 6 && currentWeaponId !== 5) playSound('shot');
                    updateHUD();

                    const raycaster = new THREE.Raycaster();
                    raycaster.setFromCamera(new THREE.Vector2(0, 0), camera);
                    
                    const enemyMeshes = enemies.flatMap(e => e.mesh.children);
                    const intersects = raycaster.intersectObjects(enemyMeshes);

                    let targetPoint = camera.position.clone().add(raycaster.ray.direction.clone().multiplyScalar(w.range));

                    if (intersects.length > 0 && intersects[0].distance <= w.range) {
                        targetPoint = intersects[0].point;
                        const hitMesh = intersects[0].object;
                        const enemyObj = enemies.find(e => e.mesh.children.includes(hitMesh) || e.mesh.children.some(c => c.children && c.children.includes(hitMesh)));
                        if (enemyObj) {
                            enemyObj.hp -= w.damage;
                            updateHUD();
                            if (enemyObj.hp <= 0) {
                                scene.remove(enemyObj.mesh);
                                enemies = enemies.filter(e => e !== enemyObj);
                                kills++;
                                money += enemyObj.isBoss ? 800 : 30;
                                if (enemyObj.isBoss) bossEnemy = null;
                                updateHUD();
                                if (enemies.length === 0) endGame(true);
                            }
                        }
                    }

                    triggerMuzzleEffect(targetPoint);
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
                }

                function endGame(victory) {
                    isGameActive = false;
                    isRoundCleared = victory;
                    gameOverScreen.style.display = 'block';

                    const title = document.getElementById('game-over-title');
                    const desc = document.getElementById('game-over-desc');
                    const btn = document.getElementById('game-over-btn');

                    if (victory) {
                        if (!roundRewardGiven) { money += 100; roundRewardGiven = true; updateHUD(); }
                        title.innerText = `라운드 ${round} 승리!`;
                        title.style.color = '#00ffcc';
                        desc.innerText = '모든 적을 처치했습니다!';
                        btn.innerText = round === 10 ? '메인 화면으로' : '다음 라운드 진입';
                    } else {
                        title.innerText = '패배했습니다...';
                        title.style.color = '#ff3333';
                        desc.innerText = '전투에서 패배했습니다.';
                        btn.innerText = '다시 시작하기';
                    }
                }

                function resetOrNextRound() {
                    gameOverScreen.style.display = 'none';
                    if (isRoundCleared && round < 10) round++;
                    else { round = 1; kills = 0; money = 0; }
                    startRound();
                    isGameActive = true;
                }

                function animate() {
                    requestAnimationFrame(animate);
                    const time = performance.now();
                    const delta = (time - prevTime) / 1000;
                    prevTime = time;

                    if (isGameActive && !isShopOpen) {
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

                        const moveSpeed = isSprinting ? 75.0 : 45.0;
                        if (moveForward || moveBackward) velocity.z -= direction.z * moveSpeed * delta;
                        if (moveLeft || moveRight) velocity.x -= direction.x * moveSpeed * delta;

                        camera.translateX(-velocity.x * delta);
                        camera.translateZ(velocity.z * delta);

                        const playerPos = camera.position;

                        for (let i = visualEffects.length - 1; i >= 0; i--) {
                            const ve = visualEffects[i];
                            ve.life -= delta;
                            if (ve.life <= 0) {
                                scene.remove(ve.mesh);
                                visualEffects.splice(i, 1);
                            }
                        }

                        for (let i = swordWaves.length - 1; i >= 0; i--) {
                            const sw = swordWaves[i];
                            sw.mesh.position.add(sw.dir.clone().multiplyScalar(sw.speed * delta));
                            sw.life -= delta;

                            if (sw.mesh.position.distanceTo(playerPos) < 2.0) {
                                playerHealth -= sw.damage;
                                updateHUD();
                                scene.remove(sw.mesh);
                                swordWaves.splice(i, 1);
                                if (playerHealth <= 0) endGame(false);
                                continue;
                            }

                            if (sw.life <= 0) {
                                scene.remove(sw.mesh);
                                swordWaves.splice(i, 1);
                            }
                        }

                        enemies.forEach(enemy => {
                            const enemyPos = enemy.mesh.position;

                            if (enemy.isBoss) {
                                if (enemy.bossType === 'dragon') {
                                    enemy.mesh.lookAt(playerPos.x, enemyPos.y, playerPos.z);

                                    if (enemy.state === 'walk') {
                                        const dist = enemyPos.distanceTo(playerPos);
                                        if (dist > 7.0) {
                                            const dir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                            enemyPos.x += dir.x * enemy.speed * delta;
                                            enemyPos.z += dir.z * enemy.speed * delta;
                                        }

                                        if (time - enemy.lastSkillTime > enemy.skillCooldown) {
                                            enemy.lastSkillTime = time;
                                            if (Math.random() > 0.4) {
                                                enemy.state = 'jumping';
                                                enemy.jumpVelocityY = 18.0;
                                            } else {
                                                const forwardDir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                                spawnDragonBreath(enemyPos, forwardDir);
                                            }
                                        }
                                    } else if (enemy.state === 'jumping') {
                                        enemy.jumpVelocityY += GRAVITY * delta;
                                        enemyPos.y += enemy.jumpVelocityY * delta;

                                        if (enemyPos.y <= 0) {
                                            enemyPos.y = 0;
                                            enemy.state = 'walk';
                                            createShockwave(enemyPos.clone(), 24.0, 40); // 넓어진 충격파 범위 (24.0)
                                        }
                                    }
                                } else if (enemy.bossType === 'blade') {
                                    enemy.mesh.lookAt(playerPos.x, enemyPos.y, playerPos.z);

                                    if (enemy.state === 'walk') {
                                        const dist = enemyPos.distanceTo(playerPos);
                                        if (dist > 3.0) {
                                            const dir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                            enemyPos.x += dir.x * enemy.speed * delta;
                                            enemyPos.z += dir.z * enemy.speed * delta;
                                        }

                                        if (time - enemy.lastSuperJumpTime > enemy.superJumpCooldown) {
                                            enemy.state = 'super_jump';
                                            enemy.lastSuperJumpTime = time;
                                            enemy.jumpVelocityY = 26.0;
                                            enemy.targetLandPos.copy(playerPos);
                                        } else if (time - enemy.lastSkillTime > enemy.skillCooldown) {
                                            enemy.lastSkillTime = time;
                                            if (Math.random() > 0.45) {
                                                enemy.state = 'charging';
                                                enemy.chargeTimer = 0;
                                                playSound('charge');
                                            } else {
                                                spawnSwordWave(enemyPos, playerPos);
                                            }
                                        }
                                    } else if (enemy.state === 'charging') {
                                        enemy.chargeTimer += delta;
                                        enemy.auraMesh.material.opacity = Math.min(0.85, enemy.chargeTimer * 0.85);

                                        if (enemy.chargeTimer >= 1.0) {
                                            enemy.state = 'dashing';
                                            enemy.auraMesh.material.opacity = 0;
                                            enemy.dashDir.subVectors(playerPos, enemyPos).normalize();
                                            enemy.chargeTimer = 0;
                                            playSound('dash');
                                        }
                                    } else if (enemy.state === 'dashing') {
                                        enemyPos.x += enemy.dashDir.x * 38.0 * delta;
                                        enemyPos.z += enemy.dashDir.z * 38.0 * delta;
                                        enemy.chargeTimer += delta;

                                        if (enemyPos.distanceTo(playerPos) < 2.5) {
                                            playerHealth -= 40;
                                            updateHUD();
                                            enemy.state = 'walk';
                                            if (playerHealth <= 0) endGame(false);
                                        } else if (enemy.chargeTimer > 0.6) {
                                            enemy.state = 'walk';
                                        }
                                    } else if (enemy.state === 'super_jump') {
                                        enemy.jumpVelocityY += GRAVITY * delta;
                                        enemyPos.y += enemy.jumpVelocityY * delta;

                                        if (enemy.jumpVelocityY < 0) enemy.state = 'dive';
                                    } else if (enemy.state === 'dive') {
                                        const dir = new THREE.Vector3().subVectors(enemy.targetLandPos, enemyPos);
                                        dir.y = 0;
                                        dir.normalize();

                                        enemyPos.x += dir.x * 28.0 * delta;
                                        enemyPos.z += dir.z * 28.0 * delta;
                                        enemyPos.y -= 40.0 * delta;

                                        if (enemyPos.y <= 0) {
                                            enemyPos.y = 0;
                                            enemy.state = 'walk';
                                            createExplosionEffect(enemyPos.clone());
                                            if (enemyPos.distanceTo(playerPos) < 7.0) {
                                                playerHealth -= 55;
                                                updateHUD();
                                                if (playerHealth <= 0) endGame(false);
                                            }
                                        }
                                    }
                                }
                            } else {
                                const dist = enemyPos.distanceTo(playerPos);
                                if (dist > 1.8) {
                                    const dir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                    enemyPos.x += dir.x * enemy.speed * delta;
                                    enemyPos.z += dir.z * enemy.speed * delta;
                                    enemy.mesh.lookAt(playerPos.x, enemyPos.y, playerPos.z);
                                } else if (time - enemy.lastAttack > 800) {
                                    playerHealth -= enemy.damage;
                                    enemy.lastAttack = time;
                                    updateHUD();
                                    if (playerHealth <= 0) endGame(false);
                                }
                            }
                        });

                        for (let i = shockwaves.length - 1; i >= 0; i--) {
                            const sw = shockwaves[i];
                            sw.currentScale += sw.expandSpeed * delta;
                            sw.mesh.scale.set(sw.currentScale, sw.currentScale, 1);
                            sw.mesh.material.opacity -= delta * 0.8;

                            if (sw.mesh.position.distanceTo(playerPos) < sw.currentScale && isGrounded) {
                                playerHealth -= sw.damage * delta * 2;
                                updateHUD();
                                if (playerHealth <= 0) endGame(false);
                            }

                            if (sw.mesh.material.opacity <= 0 || sw.currentScale >= sw.maxRadius) {
                                scene.remove(sw.mesh);
                                shockwaves.splice(i, 1);
                            }
                        }

                        for (let i = breathParticles.length - 1; i >= 0; i--) {
                            const bp = breathParticles[i];
                            bp.mesh.position.add(bp.velocity.clone().multiplyScalar(delta));
                            bp.life -= delta;

                            if (bp.mesh.position.distanceTo(playerPos) < 2.0) {
                                playerHealth -= 12 * delta;
                                updateHUD();
                                if (playerHealth <= 0) endGame(false);
                            }

                            if (bp.life <= 0) {
                                scene.remove(bp.mesh);
                                breathParticles.splice(i, 1);
                            }
                        }

                        for (let i = explosionEffects.length - 1; i >= 0; i--) {
                            const ex = explosionEffects[i];
                            ex.scale += 22.0 * delta;
                            ex.opacity -= 1.6 * delta;
                            ex.mesh.scale.set(ex.scale, ex.scale, ex.scale);
                            ex.mesh.material.opacity = ex.opacity;

                            if (ex.opacity <= 0) {
                                scene.remove(ex.mesh);
                                explosionEffects.splice(i, 1);
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
