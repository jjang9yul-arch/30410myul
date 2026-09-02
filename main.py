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
        - **상점 열기/닫기**: `B` 키
          - 🧪 체력 포션 (50G): HP +20 회복
          - 💥 산탄총 (150G) / 🔫 기관총 (300G) / 🚀 바주카포 (600G)
          - ⚡ **신규 무기** 레이저총 (1,200G): 초고속 레이저 광선 사격
        - **이동**: WASD | **재장전**: R | **무기 교체**: 1, 2, 3, 4, 5, 6 키
        - **5라운드 보스**: 크로노스 드래곤 타이탄
        - **10라운드 최종 보스**: **블레이드 마스터** (속도 재조정 및 회전하는 대검 & 퍼플 아우라 비주얼 강화)
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
                    background: linear-gradient(90deg, #a020f0, #ff0055);
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
                    background: radial-gradient(circle, rgba(0,255,255,0.8) 0%, rgba(160,32,240,0.4) 40%, rgba(0,0,0,0) 70%);
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
                    라운드: <span id="round">1</span> / 10 | 
                    체력: <span id="health" style="color: #00ffcc;">150</span> | 
                    골드: <span id="money" style="color:#ffd700;">1500</span>G | 
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
                    <h2 style="color: #ffd700; margin-top:0;">상점 & 연구소</h2>
                    <p>보유 골드: <span id="shop-money" style="color: #ffd700; font-weight: bold;">1500</span>G</p>
                    <hr style="border-color: #444;">
                    
                    <div class="buy-item">
                        <h4 style="margin: 0; color: #00ff88;">🧪 체력 포션 (Potion) - 키보드 [H]</h4>
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
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">초고속 연사 (데미지: 8 조정) | 탄창: 100발</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 300G</p>
                        <button id="buy-lmg-btn" class="buy-btn" onclick="buyWeapon(4)">기관총 구매 (300G)</button>
                    </div>

                    <div class="buy-item">
                        <h4 style="margin: 0; color: #ff3300;">🚀 바주카포 (Bazooka)</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">강력한 화력! (데미지: 180 상향) | 탄창: 1발</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 600G</p>
                        <button id="buy-bazooka-btn" class="buy-btn" onclick="buyWeapon(5)">바주카포 구매 (600G)</button>
                    </div>

                    <div class="buy-item">
                        <h4 style="margin: 0; color: #00f0ff;">⚡ 레이저총 (Laser Cannon) - 키보드 [L]</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">관통형 이펙트 레이저 사격 (데미지: 50) | 탄창: 15발</p>
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
                    } else if (type === 4) { // 기관총
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(180, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(35, audioCtx.currentTime + 0.08);
                        gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
                    } else if (type === 5) { // 바주카포
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(90, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(15, audioCtx.currentTime + 0.6);
                        gain.gain.setValueAtTime(1.0, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.6);
                    } else if (type === 6) { // 레이저총 전용 특수 사운드 (주파수 급감 효과)
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(1200, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.18);
                        gain.gain.setValueAtTime(0.6, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.18);
                    } else if (type === 'slam' || type === 'slash') {
                        osc.type = 'triangle';
                        osc.frequency.setValueAtTime(140, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 0.4);
                        gain.gain.setValueAtTime(0.8, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
                    }
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.6);
                }

                const WEAPONS = {
                    1: { name: '권총', damage: 25, range: 40, fireRate: 280, magSize: 12, reloadTime: 1200, recoil: 0.02, owned: true },
                    2: { name: '소총', damage: 55, range: 60, fireRate: 120, magSize: 30, reloadTime: 2000, recoil: 0.04, owned: true },
                    3: { name: '산탄총', damage: 18, range: 18, fireRate: 750, magSize: 6, reloadTime: 2400, recoil: 0.1, pellets: 8, owned: false, price: 150 },
                    4: { name: '기관총', damage: 8, range: 70, fireRate: 80, magSize: 100, reloadTime: 3000, recoil: 0.03, owned: false, price: 300 }, // 기관총 데미지 8로 너프
                    5: { name: '바주카포', damage: 180, range: 100, fireRate: 1500, magSize: 1, reloadTime: 2500, recoil: 0.15, owned: false, price: 600 }, // 바주카포 데미지 180으로 상향
                    6: { name: '레이저총', damage: 50, range: 120, fireRate: 150, magSize: 15, reloadTime: 1800, recoil: 0.01, owned: false, price: 1200 } // 레이저총 추가
                };

                let round = 1, kills = 0, money = 1500, playerHealth = 150, maxPlayerHealth = 150;
                let isMouseDown = false;
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
                let enemies = [], shockwaves = [], swordWaves = [], isGameActive = false, isShopOpen = false;
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

                    if (currentWeaponId === 6) { // 레이저총 3D 모델
                        const barrelGeo = new THREE.CylinderGeometry(0.08, 0.08, 0.9, 12);
                        const barrelMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, metalness: 0.9, roughness: 0.1, emissive: 0x00f0ff, emissiveIntensity: 0.5 });
                        const barrel = new THREE.Mesh(barrelGeo, barrelMat);
                        barrel.rotation.x = Math.PI / 2;
                        barrel.position.set(0.2, -0.18, -0.5);

                        const ringGeo = new THREE.TorusGeometry(0.12, 0.02, 8, 16);
                        const ringMat = new THREE.MeshBasicMaterial({ color: 0xa020f0 });
                        const ring = new THREE.Mesh(ringGeo, ringMat);
                        ring.position.set(0.2, -0.18, -0.6);

                        gunGroup.add(barrel);
                        gunGroup.add(ring);
                    } else if (currentWeaponId === 5) { // 바주카포
                        const tubeGeo = new THREE.CylinderGeometry(0.12, 0.12, 1.1, 12);
                        const tubeMat = new THREE.MeshStandardMaterial({ color: 0x223322, metalness: 0.8, roughness: 0.3 });
                        const tube = new THREE.Mesh(tubeGeo, tubeMat);
                        tube.rotation.x = Math.PI / 2;
                        tube.position.set(0.25, -0.15, -0.5);

                        const headGeo = new THREE.ConeGeometry(0.16, 0.3, 12);
                        const headMat = new THREE.MeshStandardMaterial({ color: 0xff3300, metalness: 0.5 });
                        const head = new THREE.Mesh(headGeo, headMat);
                        head.rotation.x = -Math.PI / 2;
                        head.position.set(0.25, -0.15, -1.0);

                        gunGroup.add(tube);
                        gunGroup.add(head);
                    } else if (currentWeaponId === 4) {
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
                    buySgBtn.disabled = WEAPONS[3].owned || money < WEAPONS[3].price;
                    if (WEAPONS[3].owned) buySgBtn.innerText = '보유 중 (3번 키)';

                    const buyLmgBtn = document.getElementById('buy-lmg-btn');
                    buyLmgBtn.disabled = WEAPONS[4].owned || money < WEAPONS[4].price;
                    if (WEAPONS[4].owned) buyLmgBtn.innerText = '보유 중 (4번 키)';

                    const buyBazookaBtn = document.getElementById('buy-bazooka-btn');
                    buyBazookaBtn.disabled = WEAPONS[5].owned || money < WEAPONS[5].price;
                    if (WEAPONS[5].owned) buyBazookaBtn.innerText = '보유 중 (5번 키)';

                    const buyLaserBtn = document.getElementById('buy-laser-btn');
                    buyLaserBtn.disabled = WEAPONS[6].owned || money < WEAPONS[6].price;
                    if (WEAPONS[6].owned) buyLaserBtn.innerText = '보유 중 (6번 키)';

                    const buyPotionBtn = document.getElementById('buy-potion-btn');
                    buyPotionBtn.disabled = money < 50 || playerHealth >= maxPlayerHealth;
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

                    swordWaves.forEach(sw => scene.remove(sw.mesh));
                    swordWaves = [];

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
                        document.getElementById('boss-title').innerText = "소드마스터 (블레이드 마스터)";
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

                function createEnemy(x, z) {
                    const group = new THREE.Group();

                    const torsoGeo = new THREE.ConeGeometry(0.8, 1.4, 6);
                    const armorMat = new THREE.MeshStandardMaterial({ color: 0x331122, metalness: 0.8, roughness: 0.3 });
                    const torso = new THREE.Mesh(torsoGeo, armorMat);
                    torso.rotation.x = Math.PI;
                    torso.position.y = 1.3;
                    group.add(torso);

                    const shoulderGeo = new THREE.BoxGeometry(1.6, 0.4, 0.6);
                    const shoulderMat = new THREE.MeshStandardMaterial({ color: 0x880022, metalness: 0.9, roughness: 0.2 });
                    const shoulder = new THREE.Mesh(shoulderGeo, shoulderMat);
                    shoulder.position.y = 1.8;
                    group.add(shoulder);

                    const headGeo = new THREE.OctahedronGeometry(0.4, 0);
                    const headMat = new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.9 });
                    const head = new THREE.Mesh(headGeo, headMat);
                    head.position.y = 2.2;
                    group.add(head);

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

                function createBossEnemy(x, z) {
                    const group = new THREE.Group();
                    const skinMat = new THREE.MeshStandardMaterial({ color: 0x6b1020, metalness: 0.25, roughness: 0.5 });
                    const body = new THREE.Mesh(new THREE.SphereGeometry(3.0, 20, 14), skinMat);
                    body.position.set(0, 4.0, 0);
                    group.add(body);

                    group.position.set(x, 0, z);
                    scene.add(group);

                    const maxHp = 3000;
                    bossEnemy = { mesh: group, hp: maxHp, maxHp, speed: 3.4, damage: 18, lastAttack: 0,
                        lastSlam: performance.now(), isSlamming: false, slamPhase: 0, isBoss: true, bossType: 'dragon',
                        attackIndex: 0, lastBossAttack: performance.now(), attackCooldown: 4000 };
                    enemies.push(bossEnemy);
                }

                // 10라운드 개편된 소드마스터 (보스)
                function createSwordBossEnemy(x, z) {
                    const group = new THREE.Group();

                    const armorMat = new THREE.MeshStandardMaterial({ color: 0x23232d, metalness: 0.9, roughness: 0.1 });
                    const auraMat = new THREE.MeshBasicMaterial({ color: 0xa020f0, transparent: true, opacity: 0.6, wireframe: true });
                    const swordGoldMat = new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 1.0, roughness: 0.0, emissive: 0xffd700, emissiveIntensity: 0.6 });
                    const swordCyanMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, metalness: 1.0, roughness: 0.0, emissive: 0x00f0ff, emissiveIntensity: 0.6 });

                    // 본체 및 퍼플 회전 아우라 이펙트
                    const torso = new THREE.Mesh(new THREE.BoxGeometry(1.6, 2.2, 1.0), armorMat);
                    torso.position.y = 2.5;
                    group.add(torso);

                    const head = new THREE.Mesh(new THREE.SphereGeometry(0.6, 16, 16), armorMat);
                    head.position.y = 4.0;
                    group.add(head);

                    const aura = new THREE.Mesh(new THREE.SphereGeometry(3.5, 16, 16), auraMat);
                    aura.position.y = 2.5;
                    group.add(aura);

                    // 회전하는 2개의 화려한 대검 (골드/사이언 이펙트)
                    const swordsGroup = new THREE.Group();
                    
                    const sword1 = new THREE.Mesh(new THREE.BoxGeometry(0.15, 4.0, 0.4), swordGoldMat);
                    sword1.position.set(2.2, 2.5, 0);
                    swordsGroup.add(sword1);

                    const sword2 = new THREE.Mesh(new THREE.BoxGeometry(0.15, 4.0, 0.4), swordCyanMat);
                    sword2.position.set(-2.2, 2.5, 0);
                    swordsGroup.add(sword2);

                    group.add(swordsGroup);

                    group.position.set(x, 0, z);
                    scene.add(group);

                    const maxHp = 3500;
                    bossEnemy = {
                        mesh: group,
                        swordsGroup: swordsGroup,
                        auraMesh: aura,
                        hp: maxHp,
                        maxHp: maxHp,
                        speed: 1.8, // 이동 속도 하향 조율 (천천히 다가옴)
                        damage: 25,
                        lastAttack: 0,
                        isBoss: true,
                        bossType: 'blade',
                        angle: 0,
                        state: 'idle',
                        stateTimer: 0,
                        dashTarget: new THREE.Vector3(),
                        lastBossAttack: performance.now(),
                        attackCooldown: 3000
                    };
                    enemies.push(bossEnemy);
                }

                function createSwordWave(boss) {
                    const origin = boss.mesh.position.clone().add(new THREE.Vector3(0, 2.5, 0));
                    const target = camera.position.clone();
                    const dir = new THREE.Vector3().subVectors(target, origin).normalize();

                    const geo = new THREE.TorusGeometry(2.5, 0.2, 8, 24, Math.PI);
                    const mat = new THREE.MeshBasicMaterial({ color: 0x00ffff, side: THREE.DoubleSide });
                    const wave = new THREE.Mesh(geo, mat);
                    wave.position.copy(origin);
                    wave.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
                    wave.rotation.z = Math.PI / 2;

                    scene.add(wave);

                    swordWaves.push({
                        mesh: wave,
                        direction: dir,
                        speed: 28.0,
                        damage: 30,
                        life: 2.0
                    });

                    playGunSound('slash');
                }

                function onKeyDown(e) {
                    initAudio();
                    if (!isGameActive) return;
                    if (e.code === 'KeyB') { toggleShop(); return; }
                    if (e.code === 'KeyO') { toggleFullScreen(); return; }
                    if (e.code === 'KeyM') { skipRound(); return; }
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
                        case 'Digit5': if (WEAPONS[5].owned) switchWeapon(5); break;
                        case 'Digit6': if (WEAPONS[6].owned) switchWeapon(6); break;
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
                                    money += enemyObj.isBoss ? 800 : 25;
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
                        if (round === 10) {
                            title.innerText = `🏆 최종 승리! 🏆`;
                            title.style.color = '#ffd700';
                            desc.innerText = '소드마스터를 물리치고 신화적 승리를 거두었습니다!';
                            btn.innerText = '메인 화면으로';
                        } else {
                            title.innerText = `라운드 ${round} 승리!`;
                            title.style.color = '#00ffcc';
                            desc.innerText = round % 5 === 0 ? '보스를 물리쳤습니다!' : '적을 모두 제압했습니다!';
                            btn.innerText = '다음 라운드 진입';
                        }
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
                        if (round === 10) {
                            round = 1;
                            kills = 0;
                            money = 1500;
                            WEAPONS[3].owned = false;
                            WEAPONS[4].owned = false;
                            WEAPONS[5].owned = false;
                            WEAPONS[6].owned = false;
                            currentWeaponId = 1;
                            createGunModel();
                        } else {
                            round++;
                        }
                    } else {
                        round = 1;
                        kills = 0;
                        money = 1500;
                        WEAPONS[3].owned = false;
                        WEAPONS[4].owned = false;
                        WEAPONS[5].owned = false;
                        WEAPONS[6].owned = false;
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
                        if (isMouseDown && (currentWeaponId === 4) && !isReloading) shoot();

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
                                if (enemy.bossType === 'blade') {
                                    enemy.mesh.lookAt(playerPos.x, enemyPos.y, playerPos.z);
                                    
                                    // 대검 및 아우라 회전 비주얼 이펙트
                                    if (enemy.swordsGroup) {
                                        enemy.swordsGroup.rotation.y += 4.0 * delta;
                                    }
                                    if (enemy.auraMesh) {
                                        enemy.auraMesh.rotation.z += 2.0 * delta;
                                    }

                                    const dist = enemyPos.distanceTo(playerPos);
                                    if (dist > 3.0) {
                                        const dir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                        enemyPos.x += dir.x * enemy.speed * delta; // 느려진 보스 이동 속도
                                        enemyPos.z += dir.z * enemy.speed * delta;
                                    }

                                    if (time - enemy.lastBossAttack > enemy.attackCooldown) {
                                        enemy.lastBossAttack = time;
                                        createSwordWave(enemy); // 회전 검기 스킬
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

                        // 검기 스킬 이동 및 충돌
                        for (let i = swordWaves.length - 1; i >= 0; i--) {
                            const sw = swordWaves[i];
                            sw.mesh.position.add(sw.direction.clone().multiplyScalar(sw.speed * delta));
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
