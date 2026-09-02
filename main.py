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
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🎯 Vanguard Tactical (Streamlit 3D FPS)")
    
    if "game_started" not in st.session_state:
        st.session_state.game_started = False

    if not st.session_state.game_started:
        st.subheader("메인 메뉴")
        st.write("1인칭 전술 슈팅 웹게임입니다.")
        st.markdown("""
        **주요 기능 및 조작법:**
        - **무적 모드**: 플레이어의 체력이 닳지 않습니다.
        - **골드 및 상점**: 적 처치 시 +20골드 | **상점(B 키)**에서 200골드로 기관총 구매 가능
        - **마우스 이동 / 드래그**: 시점 조준
        - **WASD**: 이동 | **Shift**: 천천히 걷기
        - **마우스 좌클릭 / Space**: 사격 (1인칭 총기 모델 및 총소리 출력)
        - **R**: 재장전 | **B**: 상점 열기/닫기
        - **1, 2, 3, 4**: 무기 교체
        """)
        
        if st.button("게임 시작", type="primary", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
    else:
        if st.button("메인 메뉴로 돌아가기"):
            st.session_state.game_started = False
            st.rerun()

        game_html = """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <style>
                body {
                    margin: 0;
                    overflow: hidden;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    user-select: none;
                    background-color: #111;
                }
                #game-container {
                    width: 100vw;
                    height: 80vh;
                    position: relative;
                    cursor: crosshair;
                }
                #hud {
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    color: #00ffcc;
                    font-size: 16px;
                    font-weight: bold;
                    text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
                    pointer-events: none;
                    z-index: 10;
                }
                #crosshair {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    width: 10px;
                    height: 10px;
                    transform: translate(-50%, -50%);
                    pointer-events: none;
                    z-index: 10;
                }
                #crosshair::before, #crosshair::after {
                    content: '';
                    position: absolute;
                    background: #00ffcc;
                }
                #crosshair::before { top: 4px; left: -5px; width: 20px; height: 2px; }
                #crosshair::after { top: -5px; left: 4px; width: 2px; height: 20px; }
                
                #start-overlay {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: white;
                    text-align: center;
                    background: rgba(0, 0, 0, 0.85);
                    padding: 25px 40px;
                    border-radius: 12px;
                    z-index: 20;
                    border: 2px solid #00ffcc;
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
                #shop-btn {
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    color: #111;
                    background-color: #ffd700;
                    border: none;
                    border-radius: 6px;
                    cursor: pointer;
                    z-index: 15;
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
                    min-width: 300px;
                    text-align: center;
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
                    background: rgba(0, 0, 0, 0.9);
                    padding: 30px;
                    border-radius: 10px;
                    z-index: 30;
                }
            </style>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        </head>
        <body>
            <div id="game-container">
                <div id="hud">
                    라운드: <span id="round">1</span> | 
                    체력: <span id="health">무적 ∞</span> | 
                    골드: <span id="money" style="color:#ffd700;">0</span>G | 
                    무기: <span id="weapon">권총</span> | 
                    탄약: <span id="ammo">12 / 12</span> | 
                    처치: <span id="kills">0</span> | 
                    남은 적: <span id="enemies-left">0</span>
                </div>
                <div id="crosshair"></div>
                
                <button id="shop-btn" onclick="toggleShop()">🛒 상점 (B)</button>

                <div id="shop-modal">
                    <h2 style="color: #ffd700; margin-top:0;">무기 상점</h2>
                    <p>현재 보유 골드: <span id="shop-money" style="color: #ffd700; font-weight: bold;">0</span>G</p>
                    <hr style="border-color: #444;">
                    <div style="margin: 15px 0; text-align: left;">
                        <h4>🔫 기관총 (LMG)</h4>
                        <p style="font-size: 12px; color: #aaa; margin: 2px 0;">데미지: 40 | 연사속도: 매우 빠름 | 탄창: 100발</p>
                        <p style="font-size: 14px; color: #ffd700; margin: 2px 0;">가격: 200G</p>
                        <button id="buy-lmg-btn" class="buy-btn" onclick="buyWeapon(4)">기관총 구매 (200G)</button>
                    </div>
                    <button onclick="toggleShop()" style="margin-top: 15px; padding: 6px 16px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">닫기</button>
                </div>
                
                <div id="start-overlay">
                    <h2>🎯 게임 준비 완료</h2>
                    <p style="color: #ccc; margin-bottom: 5px;">체력이 닳지 않는 무적 상태로 플레이합니다.</p>
                    <button id="start-btn" onclick="startGame()">전투 시작</button>
                </div>

                <div id="game-over">
                    <h1 id="game-over-title">라운드 종료</h1>
                    <button onclick="nextRound()" style="font-size: 20px; padding: 10px 20px; cursor: pointer;">다음 라운드</button>
                </div>
            </div>

            <script>
                // Web Audio API 기반 오디오 생성기
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                
                function playGunSound(type) {
                    if (audioCtx.state === 'suspended') {
                        audioCtx.resume();
                    }
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    
                    if (type === 4) { // 기관총
                        osc.type = 'sawtooth';
                        osc.frequency.setValueAtTime(120, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.12);
                        gain.gain.setValueAtTime(0.4, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.12);
                    } else if (type === 3) { // 산탄총
                        osc.type = 'square';
                        osc.frequency.setValueAtTime(80, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(20, audioCtx.currentTime + 0.25);
                        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.25);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.25);
                    } else { // 권총 및 소총
                        osc.type = 'triangle';
                        osc.frequency.setValueAtTime(200, audioCtx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.15);
                        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
                        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
                        osc.connect(gain);
                        gain.connect(audioCtx.destination);
                        osc.start();
                        osc.stop(audioCtx.currentTime + 0.15);
                    }
                }

                // 무기 옵션 설정
                const WEAPONS = {
                    1: { name: '권총', damage: 25, range: 40, fireRate: 300, magSize: 12, reloadTime: 1200, recoil: 0.02, color: 0x888888 },
                    2: { name: '소총', damage: 35, range: 60, fireRate: 120, magSize: 30, reloadTime: 2000, recoil: 0.04, color: 0x335533 },
                    3: { name: '산탄총', damage: 15, range: 15, fireRate: 800, magSize: 6, reloadTime: 2500, recoil: 0.1, pellets: 8, color: 0x553333 },
                    4: { name: '기관총', damage: 40, range: 70, fireRate: 80, magSize: 100, reloadTime: 3000, recoil: 0.03, color: 0xd4af37, owned: false }
                };

                let round = 1, kills = 0, money = 0;
                let currentWeaponId = 1, currentAmmo = WEAPONS[1].magSize;
                let isReloading = false, lastShotTime = 0;

                let scene, camera, renderer, gunMesh;
                let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false, isWalking = false;
                let prevTime = performance.now();
                let velocity = new THREE.Vector3(), direction = new THREE.Vector3();
                let enemies = [], walls = [], isGameActive = false, isShopOpen = false;

                let isMouseDown = false;
                let previousMousePosition = { x: 0, y: 0 };
                let pitch = 0, yaw = 0;

                const startOverlay = document.getElementById('start-overlay');
                const gameOverScreen = document.getElementById('game-over');

                function init() {
                    scene = new THREE.Scene();
                    scene.background = new THREE.Color(0x222233);
                    scene.fog = new THREE.Fog(0x222233, 0, 75);

                    camera = new THREE.PerspectiveCamera(75, window.innerWidth / (window.innerHeight * 0.8), 0.1, 1000);
                    camera.position.y = 1.6;

                    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
                    scene.add(ambientLight);

                    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
                    dirLight.position.set(20, 40, 20);
                    scene.add(dirLight);

                    renderer = new THREE.WebGLRenderer({ antialias: true });
                    renderer.setSize(window.innerWidth, window.innerHeight * 0.8);
                    const container = document.getElementById('game-container');
                    container.appendChild(renderer.domElement);

                    // 1인칭 총기 모델링 배치
                    createGunModel();

                    container.addEventListener('mousedown', (e) => {
                        if (isShopOpen) return;
                        isMouseDown = true;
                        previousMousePosition = { x: e.clientX, y: e.clientY };
                        if (isGameActive && e.button === 0 && !isReloading) shoot();
                    });

                    container.addEventListener('mousemove', (e) => {
                        if (!isGameActive || isShopOpen) return;

                        const deltaX = e.clientX - previousMousePosition.x;
                        const deltaY = e.clientY - previousMousePosition.y;

                        yaw -= deltaX * 0.003;
                        pitch -= deltaY * 0.003;
                        pitch = Math.max(-Math.PI / 2 + 0.1, Math.min(Math.PI / 2 - 0.1, pitch));

                        camera.rotation.order = "YXZ";
                        camera.rotation.y = yaw;
                        camera.rotation.x = pitch;

                        previousMousePosition = { x: e.clientX, y: e.clientY };
                    });

                    window.addEventListener('mouseup', () => { isMouseDown = false; });
                    document.addEventListener('keydown', onKeyDown);
                    document.addEventListener('keyup', onKeyUp);

                    buildMap();
                    startRound();
                    animate();
                }

                // 1인칭 화면에 표시되는 3D 총기 생성
                function createGunModel() {
                    if (gunMesh) camera.remove(gunMesh);

                    const gunGroup = new THREE.Group();
                    const w = WEAPONS[currentWeaponId];

                    const barrelGeo = new THREE.BoxGeometry(0.1, 0.1, 0.6);
                    const barrelMat = new THREE.MeshStandardMaterial({ color: w.color, metalness: 0.8, roughness: 0.2 });
                    const barrel = new THREE.Mesh(barrelGeo, barrelMat);
                    barrel.position.set(0.2, -0.2, -0.5);

                    const handleGeo = new THREE.BoxGeometry(0.08, 0.2, 0.08);
                    const handleMat = new THREE.MeshStandardMaterial({ color: 0x111111 });
                    const handle = new THREE.Mesh(handleGeo, handleMat);
                    handle.position.set(0.2, -0.3, -0.35);
                    handle.rotation.x = 0.2;

                    gunGroup.add(barrel);
                    gunGroup.add(handle);

                    gunMesh = gunGroup;
                    camera.add(gunMesh);
                    scene.add(camera);
                }

                function startGame() {
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
                    const floorMat = new THREE.MeshStandardMaterial({ color: 0x333333, roughness: 0.8 });
                    const floor = new THREE.Mesh(floorGeo, floorMat);
                    floor.rotation.x = -Math.PI / 2;
                    scene.add(floor);

                    const wallMat = new THREE.MeshStandardMaterial({ color: 0x555566, roughness: 0.5 });
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
                    const bodyGeo = new THREE.CylinderGeometry(0.5, 0.5, 1.8, 8);
                    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xee3333 });
                    const body = new THREE.Mesh(bodyGeo, bodyMat);
                    body.position.y = 0.9;
                    group.add(body);

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
                    
                    // 사격음 재생
                    playGunSound(currentWeaponId);
                    
                    updateHUD();

                    // 1인칭 총 반동 애니메이션
                    if (gunMesh) {
                        gunMesh.position.z += 0.05;
                        setTimeout(() => { if (gunMesh) gunMesh.position.z -= 0.05; }, 50);
                    }

                    pitch += w.recoil;

                    const raycaster = new THREE.Raycaster();
                    const count = w.pellets || 1;

                    for (let i = 0; i < count; i++) {
                        const spreadX = (Math.random() - 0.5) * (w.recoil);
                        const spreadY = (Math.random() - 0.5) * (w.recoil);
                        raycaster.setFromCamera(new THREE.Vector2(spreadX, spreadY), camera);
                        
                        const enemyMeshes = enemies.map(e => e.mesh.children[0]);
                        const intersects = raycaster.intersectObjects(enemyMeshes);

                        if (intersects.length > 0 && intersects[0].distance <= w.range) {
                            const hitMesh = intersects[0].object;
                            const enemyObj = enemies.find(e => e.mesh.children[0] === hitMesh);
                            if (enemyObj) {
                                enemyObj.hp -= w.damage;
                                if (enemyObj.hp <= 0) {
                                    scene.remove(enemyObj.mesh);
                                    enemies = enemies.filter(e => e !== enemyObj);
                                    kills++;
                                    money += 20; // 적 처치 시 20골드 지급
                                    updateHUD();
                                    if (enemies.length === 0) endRound(true);
                                }
                            }
                        }
                    }
                }

                function updateHUD() {
                    document.getElementById('round').innerText = round;
                    document.getElementById('money').innerText = money;
                    document.getElementById('weapon').innerText = WEAPONS[currentWeaponId].name;
                    document.getElementById('ammo').innerText = `${currentAmmo} / ${WEAPONS[currentWeaponId].magSize}`;
                    document.getElementById('kills').innerText = kills;
                    document.getElementById('enemies-left').innerText = enemies.length;
                }

                function endRound(victory) {
                    isGameActive = false;
                    gameOverScreen.style.display = 'block';
                    const title = document.getElementById('game-over-title');
                    title.innerText = `라운드 ${round} 승리!`;
                    title.style.color = '#00ffcc';
                }

                function nextRound() {
                    gameOverScreen.style.display = 'none';
                    round++;
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
                        
                        // 적 AI 이동 (무적 상태이므로 공격을 받아도 체력이 감소하지 않음)
                        enemies.forEach(enemy => {
                            const enemyPos = enemy.mesh.position;
                            const dist = enemyPos.distanceTo(playerPos);

                            if (dist > 1.5) {
                                const dir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                enemyPos.x += dir.x * enemy.speed * delta;
                                enemyPos.z += dir.z * enemy.speed * delta;
                                enemy.mesh.lookAt(playerPos.x, enemyPos.y, playerPos.z);
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
        
        components.html(game_html, height=750)

if __name__ == "__main__":
    main()
