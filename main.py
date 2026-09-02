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
        **업데이트 내용 및 조작법:**
        - **체력 시스템**: 적 공격 시 체력 감소 (0이 되면 패배)
        - **전체 화면 지원**: 오른쪽 상단 [전체 화면] 버튼으로 마우스 이탈 방지
        - **마우스 이동**: 시점 조준
        - **WASD**: 이동 | **Shift**: 천천히 걷기
        - **마우스 좌클릭 / Space**: 사격 (개선된 오디오 및 기관총 전용 모델)
        - **R**: 재장전 | **B**: 상점 열기/닫기 (200G로 기관총 구매)
        - **1, 2, 3, 4**: 무기 교체
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
                    background-color: #111;
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
                    box-shadow: 0 0 4px #00ffcc;
                }
                #crosshair::after {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 9px;
                    width: 2px;
                    height: 20px;
                    background: #00ffcc;
                    box-shadow: 0 0 4px #00ffcc;
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
                    background: rgba(0, 0, 0, 0.88);
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
                    min-width: 320px;
                    text-align: center;
                    cursor: default;
                }
                .buy-btn {
                    margin-top: 10px;
                    padding: 8px 16px;
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
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
                
                <div id="top-controls">
                    <button id="shop-btn" class="ui-btn" onclick="toggleShop()">🛒 상점 (B)</button>
                    <button id="fullscreen-btn" class="ui-btn" onclick="toggleFullScreen()">🖥️ 전체 화면</button>
                </div>

                <div id="shop-modal">
                    <h2 style="color: #ffd700; margin-top:0;">무기 상점</h2>
                    <p>현재 보유 골드: <span id="shop-money" style="color: #ffd700; font-weight: bold;">0</span>G</p>
                    <hr style="border-color: #444;">
                    <div style="margin: 15px 0; text-align: left;">
                        <h4>🔫 기관총 (LMG)</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">골드 모델링 | 높은 연사 속도 | 탄창: 100발</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 200G</p>
                        <button id="buy-lmg-btn" class="buy-btn" onclick="buyWeapon(4)">기관총 구매 (200G)</button>
                    </div>
                    <button onclick="toggleShop()" style="margin-top: 15px; padding: 6px 16px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">닫기</button>
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
                    
                    if (type === 4) {
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(160, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.1);
                        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.1);
                    } else if (type === 3) {
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(90, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.2);
                        gain.gain.setValueAtTime(0.6, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.2);
                    } else {
                        osc.type = 'triangle';
                        osc.frequency.setValueAtTime(220, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.12);
                        gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.12);
                    }
                }

                const WEAPONS = {
                    1: { name: '권총', damage: 25, range: 40, fireRate: 300, magSize: 12, reloadTime: 1200, recoil: 0.02, color: 0x777777 },
                    2: { name: '소총', damage: 35, range: 60, fireRate: 120, magSize: 30, reloadTime: 2000, recoil: 0.04, color: 0x225522 },
                    3: { name: '산탄총', damage: 15, range: 15, fireRate: 800, magSize: 6, reloadTime: 2500, recoil: 0.1, pellets: 8, color: 0x552222 },
                    4: { name: '기관총', damage: 40, range: 70, fireRate: 80, magSize: 100, reloadTime: 3000, recoil: 0.03, color: 0xd4af37, owned: false }
                };

                let round = 1, kills = 0, money = 0, playerHealth = 100;
                let currentWeaponId = 1, currentAmmo = WEAPONS[1].magSize;
                let isReloading = false, lastShotTime = 0;

                let scene, camera, renderer, gunMesh;
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
                    scene.background = new THREE.Color(0x1a1a24);
                    scene.fog = new THREE.Fog(0x1a1a24, 0, 75);

                    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                    camera.position.y = 1.6;

                    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
                    scene.add(ambientLight);

                    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
                    dirLight.position.set(20, 40, 20);
                    scene.add(dirLight);

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

                    if (currentWeaponId === 4) {
                        const bodyGeo = new THREE.BoxGeometry(0.16, 0.18, 0.8);
                        const bodyMat = new THREE.MeshStandardMaterial({ color: 0xd4af37, metalness: 0.9, roughness: 0.2 });
                        const body = new THREE.Mesh(bodyGeo, bodyMat);
                        body.position.set(0.22, -0.2, -0.5);

                        const magGeo = new THREE.BoxGeometry(0.12, 0.22, 0.2);
                        const magMat = new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.5 });
                        const mag = new THREE.Mesh(magGeo, magMat);
                        mag.position.set(0.22, -0.32, -0.45);

                        gunGroup.add(body);
                        gunGroup.add(mag);
                    } else {
                        const barrelGeo = new THREE.BoxGeometry(0.1, 0.1, 0.55);
                        const barrelMat = new THREE.MeshStandardMaterial({ color: w.color, metalness: 0.7, roughness: 0.3 });
                        const barrel = new THREE.Mesh(barrelGeo, barrelMat);
                        barrel.position.set(0.2, -0.2, -0.45);

                        gunGroup.add(barrel);
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
                    
                    const buyBtn = document.getElementById('buy-lmg-btn');
                    if (WEAPONS[4].owned) {
                        buyBtn.innerText = '보유 중 (4번 키로 장착)';
                        buyBtn.disabled = true;
                    } else {
                        buyBtn.disabled = money < 200;
                    }
                }

                function buyWeapon(id) {
                    if (money >= 200 && !WEAPONS[id].owned) {
                        money -= 200;
                        WEAPONS[id].owned = true;
                        switchWeapon(id);
                        toggleShop();
                        updateHUD();
                    }
                }

                function buildMap() {
                    const floorGeo = new THREE.PlaneGeometry(100, 100);
                    const floorMat = new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.8 });
                    const floor = new THREE.Mesh(floorGeo, floorMat);
                    floor.rotation.x = -Math.PI / 2;
                    scene.add(floor);

                    const wallMat = new THREE.MeshStandardMaterial({ color: 0x444455, roughness: 0.5 });
                    const createBox = (w, h, d, x, y, z) => {
                        const geo = new THREE.BoxGeometry(w, h, d);
                        const mesh = new THREE.Mesh(geo, wallMat);
                        mesh.position.set(x, y, z);
                        scene.add(mesh);
                        walls.push(mesh);
                    };

                    createBox(100, 10, 2, 0, 5, -50);
                    createBox(100, 10, 2, 0, 5, 50);
                    createBox(2, 10, 100, -50, 5, 0);
                    createBox(2, 10, 100, 50, 5, 0);
                    createBox(20, 6, 4, -15, 3, -10);
                    createBox(4, 6, 20, 15, 3, 10);
                    createBox(12, 6, 12, 0, 3, 0);
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
                    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xcc2222, metalness: 0.5 });
                    const body = new THREE.Mesh(bodyGeo, bodyMat);
                    body.position.y = 1.0;
                    group.add(body);

                    const headGeo = new THREE.BoxGeometry(0.4, 0.4, 0.4);
                    const headMat = new THREE.MeshStandardMaterial({ color: 0x111111 });
                    const head = new THREE.Mesh(headGeo, headMat);
                    head.position.y = 1.8;
                    group.add(head);

                    const gunGeo = new THREE.BoxGeometry(0.1, 0.1, 0.6);
                    const gunMat = new THREE.MeshStandardMaterial({ color: 0x333333 });
                    const gun = new THREE.Mesh(gunGeo, gunMat);
                    gun.position.set(0.45, 1.0, -0.3);
                    group.add(gun);

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
                    if (isShopOpen) return;

                    switch (e.code) {
                        case 'KeyW': moveForward = true; break;
                        case 'KeyS': moveBackward = true; break;
                        case 'KeyA': moveLeft = true; break;
                        case 'KeyD': moveRight = true; break;
                        case 'ShiftLeft': isWalking = true; break;
                        case 'KeyR': reload(); break;
                        case 'Space': shoot(); break;
                        case 'Digit1': switchWeapon(1); break;
                        case 'Digit2': switchWeapon(2); break;
                        case 'Digit3': switchWeapon(3); break;
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

                function shoot() {
                    const now = performance.now();
                    const w = WEAPONS[currentWeaponId];
                    if (now - lastShotTime < w.fireRate) return;
                    if (currentAmmo <= 0) { reload(); return; }

                    lastShotTime = now;
                    currentAmmo--;
                    
                    playGunSound(currentWeaponId);
                    updateHUD();

                    if (gunMesh) {
                        gunMesh.position.z += 0.06;
                        setTimeout(() => { if (gunMesh) gunMesh.position.z -= 0.06; }, 40);
                    }

                    pitch += w.recoil;

                    const raycaster = new THREE.Raycaster();
                    const count = w.pellets || 1;

                    for (let i = 0; i < count; i++) {
                        const spreadX = (Math.random() - 0.5) * (w.recoil);
                        const spreadY = (Math.random() - 0.5) * (w.recoil);
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
                                    money += 20;
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
                        desc.innerText = '적을 모두 물리쳤습니다!';
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
                                // 적 근접 공격 및 데미지 연산 (1초 간격)
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
