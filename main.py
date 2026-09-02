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
        - **사격**: 마우스 좌클릭 / `Space` / `J` 키
        - **전체 화면 전환**: `O` 키 또는 오른쪽 상단 버튼
        - **상점 열기/닫기**: `B` 키 (산탄총 150G / 기관총 300G)
        - **이동**: WASD | **천천히 걷기**: Shift | **재장전**: R
        - **무기 교체**: 1, 2, 3, 4 키
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
                    
                    if (type === 1) { // 권총
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(320, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.12);
                        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.12);
                    } else if (type === 2) { // 소총
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(240, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.15);
                        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.15);
                    } else if (type === 3) { // 산탄총
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(120, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.25);
                        gain.gain.setValueAtTime(0.7, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.25);
                    } else if (type === 4) { // 기관총
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(180, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(35, audioCtx.currentTime + 0.08);
                        gain.gain.setValueAtTime(0.6, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.08);
                    }
                }

                const WEAPONS = {
                    1: { name: '권총', damage: 25, range: 40, fireRate: 280, magSize: 12, reloadTime: 1200, recoil: 0.02, color: 0xdddddd, owned: true },
                    2: { name: '소총', damage: 35, range: 60, fireRate: 120, magSize: 30, reloadTime: 2000, recoil: 0.04, color: 0x33aa33, owned: true },
                    3: { name: '산탄총', damage: 16, range: 18, fireRate: 750, magSize: 6, reloadTime: 2400, recoil: 0.1, pellets: 8, color: 0xff6600, owned: false, price: 150 },
                    4: { name: '기관총', damage: 40, range: 70, fireRate: 80, magSize: 100, reloadTime: 3000, recoil: 0.03, color: 0xffd700, owned: false, price: 300 }
                };

                let round = 1, kills = 0, money = 0, playerHealth = 100;
                let currentWeaponId = 1, currentAmmo = WEAPONS[1].magSize;
                let isReloading = false, lastShotTime = 0;

                let scene, camera, renderer, gunMesh, muzzleLight;
                let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false, isWalking = false;
                let prevTime = performance.now();
                let velocity = new THREE.Vector3(), direction = new THREE.Vector3();
                let enemies = [], walls = [], isGameActive = false, isShopOpen = false;
                let isRoundCleared = false;

                let pitch = 0, yaw = 0;

                const startOverlay = document.getElementById('start-overlay');
                const gameOverScreen = document.getElementById('game-over');

                function init() {
                    scene = new THREE.Scene();
                    scene.background = new THREE.Color(0x050510);
                    scene.fog = new THREE.FogExp2(0x050510, 0.02);

                    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                    camera.position.y = 1.6;

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
                        if (isGameActive && e.button === 0 && !isReloading) shoot();
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
                    const w = WEAPONS[currentWeaponId];

                    if (currentWeaponId === 4) { // 기관총
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
                    } else if (currentWeaponId === 3) { // 산탄총
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
                    } else if (currentWeaponId === 2) { // 소총
                        const barrelGeo = new THREE.BoxGeometry(0.1, 0.12, 0.65);
                        const barrelMat = new THREE.MeshStandardMaterial({ color: 0x00ffcc, metalness: 0.8, roughness: 0.2 });
                        const barrel = new THREE.Mesh(barrelGeo, barrelMat);
                        barrel.position.set(0.2, -0.2, -0.45);

                        gunGroup.add(barrel);
                    } else { // 권총
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

                function buildMap() {
                    // 화려한 사이버펑크 스타일 맵
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
                        walls.push(mesh);
                    };

                    // 외곽 벽 (네온 시안)
                    createWall(100, 10, 2, 0, 5, -50, 0x112233);
                    createWall(100, 10, 2, 0, 5, 50, 0x112233);
                    createWall(2, 10, 100, -50, 5, 0, 0x112233);
                    createWall(2, 10, 100, 50, 5, 0, 0x112233);

                    // 내부 장애물 (화려한 보라/주황 네온)
                    createWall(20, 6, 4, -15, 3, -10, 0x440066);
                    createWall(4, 6, 20, 15, 3, 10, 0x663300);
                    createWall(12, 6, 12, 0, 3, 0, 0x004466);
                }

                function startRound() {
                    enemies.forEach(e => scene.remove(e.mesh));
                    enemies = [];
                    playerHealth = 100;
                    camera.position.set(0, 1.6, 40);
                    
                    const enemyCount = round * 2 + 1;
                    const spawnPositions = [
                        {x: -30, z: -30}, {x: 0, z: -35}, {x: 30, z: -30},
                        {x: -25, z: 0}, {x: 25, z: 0}
                    ];

                    for (let i = 0; i < enemyCount; i++) {
                        const pos = spawnPositions[i % spawnPositions.length];
                        createEnemy(pos.x + (Math.random()*4 - 2), pos.z + (Math.random()*4 - 2));
                    }
                    updateHUD();
                }

                function createEnemy(x, z) {
                    const group = new THREE.Group();

                    const bodyGeo = new THREE.BoxGeometry(0.8, 1.2, 0.5);
                    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xff0044, metalness: 0.5 });
                    const body = new THREE.Mesh(bodyGeo, bodyMat);
                    body.position.y = 1.0;
                    group.add(body);

                    const headGeo = new THREE.BoxGeometry(0.4, 0.4, 0.4);
                    const headMat = new THREE.MeshStandardMaterial({ color: 0xffff00 });
                    const head = new THREE.Mesh(headGeo, headMat);
                    head.position.y = 1.8;
                    group.add(head);

                    group.position.set(x, 0, z);
                    scene.add(group);

                    enemies.push({
                        mesh: group,
                        hp: 50 + (round * 10),
                        maxHp: 50 + (round * 10),
                        speed: 3 + (Math.random() * 1.5),
                        damage: 10,
                        lastAttack: 0
                    });
                }

                function onKeyDown(e) {
                    initAudio();
                    if (!isGameActive) return;
                    if (e.code === 'KeyB') { toggleShop(); return; }
                    if (e.code === 'KeyO') { toggleFullScreen(); return; }
                    if (isShopOpen) return;

                    switch (e.code) {
                        case 'KeyW': moveForward = true; break;
                        case 'KeyS': moveBackward = true; break;
                        case 'KeyA': moveLeft = true; break;
                        case 'KeyD': moveRight = true; break;
                        case 'ShiftLeft': isWalking = true; break;
                        case 'KeyR': reload(); break;
                        case 'Space': 
                        case 'KeyJ': shoot(); break;
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
                        case 'ShiftLeft': isWalking = false; break;
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
                    // HUD 이펙트
                    const flash = document.getElementById('muzzle-flash-hud');
                    flash.style.display = 'block';
                    setTimeout(() => { flash.style.display = 'none'; }, 40);

                    // 3D 조명 이펙트
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
                                if (enemyObj.hp <= 0) {
                                    scene.remove(enemyObj.mesh);
                                    enemies = enemies.filter(e => e !== enemyObj);
                                    kills++;
                                    money += 25;
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
                        title.innerText = `라운드 ${round} 승리!`;
                        title.style.color = '#00ffcc';
                        desc.innerText = '적을 모두 제압했습니다!';
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
                        velocity.x -= velocity.x * 10.0 * delta;
                        velocity.z -= velocity.z * 10.0 * delta;

                        direction.z = Number(moveForward) - Number(moveBackward);
                        direction.x = Number(moveRight) - Number(moveLeft);
                        direction.normalize();

                        const moveSpeed = isWalking ? 15.0 : 35.0;
                        if (moveForward || moveBackward) velocity.z -= direction.z * moveSpeed * delta;
                        if (moveLeft || moveRight) velocity.x -= direction.x * moveSpeed * delta;

                        camera.translateX(-velocity.x * delta);
                        camera.translateZ(velocity.z * delta);
                        camera.position.y = 1.6;

                        const playerPos = camera.position;
                        
                        enemies.forEach(enemy => {
                            const enemyPos = enemy.mesh.position;
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
                        });
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
