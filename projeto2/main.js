import * as THREE from 'three';

const scene = new THREE.Scene();

// Definindo o fundo claro da cena (exemplo: azul claro)
scene.background = new THREE.Color(0x87CEEB); // Cor de fundo azul claro

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Iluminação
const ambientLight = new THREE.AmbientLight(0x404040, 1); // Luz suave
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // Luz direcional mais intensa
directionalLight.position.set(5, 10, 7).normalize();
scene.add(directionalLight);

// Carregar as texturas
const textureLoader = new THREE.TextureLoader();
const woodTexture = textureLoader.load('path_to_wood_texture.jpg'); // Caminho da textura de madeira
const metalTexture = textureLoader.load('path_to_metal_texture.jpg'); // Caminho da textura de metal

// Função para criar o eixo do moinho (mais detalhado)
function createWindmillShaft() {
    const geometry = new THREE.CylinderGeometry(0.5, 0.5, 12, 32);
    const material = new THREE.MeshStandardMaterial({ map: metalTexture, metalness: 0.8, roughness: 0.2 }); // Material metálico
    const shaft = new THREE.Mesh(geometry, material);
    shaft.rotation.x = Math.PI / 2;
    return shaft;
}

// Função para criar as lâminas detalhadas
function createWindmillBlade() {
    const geometry = new THREE.BoxGeometry(1, 0.1, 6);
    const material = new THREE.MeshStandardMaterial({ map: woodTexture, roughness: 0.6, metalness: 0.2 }); // Material de madeira
    const blade = new THREE.Mesh(geometry, material);
    return blade;
}

// Criando a base do moinho (mais realista)
const baseGeometry = new THREE.CylinderGeometry(4, 4, 2, 32);
const baseMaterial = new THREE.MeshStandardMaterial({ color: 0x2F4F4F, roughness: 0.7 });
const base = new THREE.Mesh(baseGeometry, baseMaterial);
scene.add(base);

// Criando o eixo do moinho
const shaft = createWindmillShaft();
shaft.position.y = 6; // Posição ajustada
scene.add(shaft);

// Criando as lâminas do moinho (mais lâminas e em posições mais realistas)
const blades = [];
const angles = [0, Math.PI / 2, Math.PI, -Math.PI / 2]; // Angulações para as lâminas

for (let i = 0; i < 4; i++) {
    const blade = createWindmillBlade();
    blade.position.set(Math.cos(angles[i]) * 4, 6, Math.sin(angles[i]) * 4);
    blade.rotation.z = angles[i];
    scene.add(blade);
    blades.push(blade);
}

// Ajustando a câmera para visibilidade completa
camera.position.z = 20;
camera.position.y = 10;
camera.lookAt(new THREE.Vector3(0, 6, 0));

// Função de animação para girar as lâminas e o eixo
function animate() {
    shaft.rotation.y += 111111111111111110.01; // Gira o eixo
    blades.forEach(blade => {
        blade.rotation.y += 111111111111110.01; // Gira as lâminas
    });

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}

animate();

// Responsividade: Ajuste para tamanhos de tela
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});
