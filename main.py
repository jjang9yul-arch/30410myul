import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정
st.set_page_config(
    page_title="Vanguard Tactical 3D",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS (Streamlit 여백 제거 및 풀스크린 스타일ing)
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
    
    # 세션 상태 초기화
    if "game_started" not in st.session_state:
        st.session_state.game_started = False

    if not st.session_state.game_started:
        st.subheader("메인 메뉴")
        st.write("발로란트 스타일의 1인칭 전술 슈팅 웹게임입니다.")
        st.markdown("""
        **조작 방법:**
        - **화면 클릭**: 조준경 잠금 (마우스 조준 활성화)
        - **WASD**: 이동 | **Shift**: 천천히 걷기
        - **마우스 왼쪽 클릭**: 발사
        - **R**: 재장전
        - **1, 2, 3**: 무기 교체 (1: 권총, 2: 소총, 3: 산탄총)
        - **Esc**: 마우스 커서 해제
        """)
        
        if st.button("게임 시작", type="primary", use_container_width=True):
            st.session_state.game_started = True
            st.rerun()
    else:
        if st.button("메인 메뉴로 돌아가기"):
            st.session_state.game_started = False
            st.rerun()

        # Three.js 기반 3D FPS 게임 임베딩 (HTML/JS/CSS 통합)
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
                #crosshair::before {
                    top: 4px; left: -5px; width: 20px; height: 2px;
                }
                #crosshair::after {
                    top: -5px; left: 4px; width: 2px; height: 20px;
                }
                #instructions {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    color: white;
                    text-align: center;
                    font-size: 24px;
                    background: rgba(0, 0, 0, 0.7);
                    padding: 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    z-index: 20;
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
                    background: rgba(0, 0, 0, 0.85);
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
                    체력: <span id="health">100</span> | 
                    무기: <span id="weapon">권총</span> | 
                    탄약: <span id="ammo">12 / 12</span> | 
                    처치: <span id="kills">0</span> | 
                    남은 적: <span id="enemies-left">0</span>
                </div>
                <div id="crosshair"></div>
                <div id="instructions">화면을 클릭하여 게임을 시작하세요 (마우스 조준 활성화)</div>
                <div id="game-over">
                    <h1 id="game-over-title">라운드 종료</h1>
                    <button onclick="nextRound()" style="font-size: 20px; padding: 10px 20px; cursor: pointer;">다음 라운드</button>
                </div>
            </div>

            <script>
                // 무기 데이터 설정
                const WEAPONS = {
                    1: { name: '권총', damage: 25, range: 40, fireRate: 300, magSize: 12, reloadTime: 1200, recoil: 0.02 },
                    2: { name: '소총', damage: 35, range: 60, fireRate: 120, magSize: 30, reloadTime: 2000, recoil: 0.04 },
                    3: { name: '산탄총', damage: 15, range: 15, fireRate: 800, magSize: 6, reloadTime: 2500, recoil: 0.1, pellets: 8 }
                };

                // 게임 상태 변수
                let round = 1;
                let playerHealth = 100;
                let kills = 0;
                let currentWeaponId = 1;
                let currentAmmo = WEAPONS[1].magSize;
                let isReloading = false;
                let lastShotTime = 0;

                let scene, camera, renderer;
                let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false, isWalking = false;
                let prevTime = performance.now();
                let velocity = new THREE.Vector3();
                let direction = new THREE.Vector3();

                let enemies = [];
                let walls = [];
                let isGameActive = false;

                const instructions = document.getElementById('instructions');
                const gameOverScreen = document.getElementById('game-over');

                function init() {
                    // 씬 및 카메라 설정
                    scene = new THREE.Scene();
                    scene.background = new THREE.Color(0x222233);
                    scene.fog = new THREE.Fog(0x222233, 0, 75);

                    camera = new THREE.PerspectiveCamera(75, window.innerWidth / (window.innerHeight * 0.8), 0.1, 1000);
                    camera.position.y = 1.6; // 플레이어 눈높이

                    // 조명 설정
                    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
                    scene.add(ambientLight);

                    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
                    dirLight.position.set(20, 40, 20);
                    scene.add(dirLight);

                    // 렌더러 설정
                    renderer = new THREE.WebGLRenderer({ antialias: true });
                    renderer.setSize(window.innerWidth, window.innerHeight * 0.8);
                    document.getElementById('game-container').appendChild(renderer.domElement);

                    // 포인터락 (마우스 시점 제어)
                    instructions.addEventListener('click', function () {
                        document.body.requestPointerLock();
                    });

                    document.addEventListener('pointerlockchange', function () {
                        if (document.pointerLockElement === document.body) {
                            instructions.style.display = 'none';
                            isGameActive = true;
                        } else {
                            if (playerHealth > 0) {
                                instructions.style.display = 'block';
                            }
                            isGameActive = false;
                        }
                    });

                    document.addEventListener('mousemove', onMouseMove);
                    document.addEventListener('keydown', onKeyDown);
                    document.addEventListener('keyup', onKeyUp);
                    document.addEventListener('mousedown', onMouseDown);

                    // 맵 생성
                    buildMap();

                    // 첫 라운드 시작
                    startRound();

                    animate();
                }

                // 맵 및 구조물 생성
                function buildMap() {
                    // 바닥
                    const floorGeo = new THREE.PlaneGeometry(100, 100);
                    const floorMat = new THREE.MeshStandardMaterial({ color: 0x333333, roughness: 0.8 });
                    const floor = new THREE.Mesh(floorGeo, floorMat);
                    floor.rotation.x = -Math.PI / 2;
                    scene.add(floor);

                    // 외벽 및 장애물
                    const wallMat = new THREE.MeshStandardMaterial({ color: 0x555566, roughness: 0.5 });
                    
                    const createBox = (w, h, d, x, y, z) => {
                        const geo = new THREE.BoxGeometry(w, h, d);
                        const mesh = new THREE.Mesh(geo, wallMat);
                        mesh.position.set(x, y, z);
                        scene.add(mesh);
                        walls.push(mesh);
                    };

                    // 외벽
                    createBox(100, 10, 2, 0, 5, -50);
                    createBox(100, 10, 2, 0, 5, 50);
                    createBox(2, 10, 100, -50, 5, 0);
                    createBox(2, 10, 100, 50, 5, 0);

                    // 내부 장애물/통로
                    createBox(20, 6, 4, -15, 3, -10);
                    createBox(4, 6, 20, 15, 3, 10);
                    createBox(12, 6, 12, 0, 3, 0);
                }

                // 라운드 설정 및 적 스폰
                function startRound() {
                    // 기존 적 제거
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

                // 적 AI 생성
                function createEnemy(x, z) {
                    const group = new THREE.Group();
                    
                    // 적 몸통
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

                // 입력 이벤트 처리
                function onKeyDown(e) {
                    switch (e.code) {
                        case 'KeyW': moveForward = true; break;
                        case 'KeyS': moveBackward = true; break;
                        case 'KeyA': moveLeft = true; break;
                        case 'KeyD': moveRight = true; break;
                        case 'ShiftLeft': isWalking = true; break;
                        case 'KeyR': reload(); break;
                        case 'Digit1': switchWeapon(1); break;
                        case 'Digit2': switchWeapon(2); break;
                        case 'Digit3': switchWeapon(3); break;
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

                let pitch = 0, yaw = 0;
                function onMouseMove(e) {
                    if (document.pointerLockElement !== document.body) return;

                    const movementX = e.movementX || 0;
                    const movementY = e.movementY || 0;

                    yaw -= movementX * 0.002;
                    pitch -= movementY * 0.002;

                    pitch = Math.max(-Math.PI / 2 + 0.1, Math.min(Math.PI / 2 - 0.1, pitch));

                    camera.rotation.order = "YXZ";
                    camera.rotation.y = yaw;
                    camera.rotation.x = pitch;
                }

                function switchWeapon(id) {
                    if (isReloading || currentWeaponId === id) return;
                    currentWeaponId = id;
                    currentAmmo = WEAPONS[id].magSize;
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

                function onMouseDown(e) {
                    if (e.button === 0 && isGameActive && !isReloading) {
                        shoot();
                    }
                }

                // 사격 로직
                function shoot() {
                    const now = performance.now();
                    const w = WEAPONS[currentWeaponId];

                    if (now - lastShotTime < w.fireRate) return;
                    if (currentAmmo <= 0) {
                        reload();
                        return;
                    }

                    lastShotTime = now;
                    currentAmmo--;
                    updateHUD();

                    // 반동 표현 (카메라 살짝 흔들림)
                    pitch += w.recoil;

                    // 광선 투사(Raycasting) 사격 검사
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
                                    updateHUD();

                                    if (enemies.length === 0) {
                                        endRound(true);
                                    }
                                }
                            }
                        }
                    }
                }

                function updateHUD() {
                    document.getElementById('round').innerText = round;
                    document.getElementById('health').innerText = Math.max(0, Math.round(playerHealth));
                    document.getElementById('weapon').innerText = WEAPONS[currentWeaponId].name;
                    document.getElementById('ammo').innerText = `${currentAmmo} / ${WEAPONS[currentWeaponId].magSize}`;
                    document.getElementById('kills').innerText = kills;
                    document.getElementById('enemies-left').innerText = enemies.length;
                }

                function endRound(victory) {
                    isGameActive = false;
                    document.exitPointerLock();
                    
                    gameOverScreen.style.display = 'block';
                    const title = document.getElementById('game-over-title');
                    if (victory) {
                        title.innerText = `라운드 ${round} 승리!`;
                        title.style.color = '#00ffcc';
                    } else {
                        title.innerText = '패배했습니다...';
                        title.style.color = '#ff3333';
                    }
                }

                function nextRound() {
                    gameOverScreen.style.display = 'none';
                    if (playerHealth <= 0) {
                        round = 1;
                        kills = 0;
                    } else {
                        round++;
                    }
                    startRound();
                }

                // 메인 게임 루프 (60 FPS)
                function animate() {
                    requestAnimationFrame(animate);

                    const time = performance.now();
                    const delta = (time - prevTime) / 1000;
                    prevTime = time;

                    if (isGameActive && playerHealth > 0) {
                        // 플레이어 이동 로직
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
                        camera.position.y = 1.6; // Y축 고정

                        // 적 AI 업데이트
                        const playerPos = camera.position;
                        enemies.forEach(enemy => {
                            const enemyPos = enemy.mesh.position;
                            const dist = enemyPos.distanceTo(playerPos);

                            if (dist > 1.5) {
                                // 플레이어 방향으로 추적
                                const dir = new THREE.Vector3().subVectors(playerPos, enemyPos).normalize();
                                enemyPos.x += dir.x * enemy.speed * delta;
                                enemyPos.z += dir.z * enemy.speed * delta;
                                enemy.mesh.lookAt(playerPos.x, enemyPos.y, playerPos.z);
                            } else {
                                // 사정거리 내 공격
                                if (time - enemy.lastAttack > 1000) {
                                    playerHealth -= enemy.damage;
                                    enemy.lastAttack = time;
                                    updateHUD();

                                    if (playerHealth <= 0) {
                                        endRound(false);
                                    }
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
        
        components.html(game_html, height=700)

if __name__ == "__main__":
    main();
