var contenedor;

var camera, scene, renderer;

var axes = new THREE.AxesHelper(50);

var mesh;


var inclinacionX;
var inclinacionY;
var inclinacionZ;


init();
animate()

function init() {

	contenedor = document.getElementById('attitude');
	scene = new THREE.Scene();
	camera = new THREE.PerspectiveCamera(2.5, 200/150, 1, 2000 );
	//camera.up.set(0,1,0);
	// scene

	

	var ambient = new THREE.AmbientLight( 0x444444 );
	scene.add( ambient );

	var directionalLight = new THREE.DirectionalLight( 0xffeeff );
	directionalLight.position.set( 0, 0, 1 ).normalize();
	scene.add( directionalLight );
	scene.add( axes );

	//var axesHelper = new THREE.AxesHelper( 10 );
	//scene.add( axesHelper );
	


	THREE.Loader.Handlers.add( /\.dds$/i, new THREE.DDSLoader() );

	var mtlLoader = new THREE.MTLLoader();
	mtlLoader.load( '', function( materials ) {
		materials.preload();

		var objLoader = new THREE.OBJLoader();
		objLoader.setMaterials( materials );
		objLoader.load( '../static/E3Tratos/assets/js/model/gondola2.obj', function ( object ) {
			object.children[0].geometry.computeFaceNormals();
            var  geometry = object.children[0].geometry;
            
            //THREE.GeometryUtils.center(geometry);
            geometry.center()
            geometry.dynamic = true;
            var material = new THREE.MeshLambertMaterial({color: 0xffffff});
            mesh = new THREE.Mesh(geometry, material);  
            scene.add( mesh )
		});
			
		scene.background = new THREE.Color( 0x22282d );

	});

	renderer = new THREE.WebGLRenderer();
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( 200, 150 );
	contenedor.appendChild( renderer.domElement );

	//window.addEventListener( 'resize', onWindowResize, false );
	
}

function onWindowResize() {

	windowHalfX = window.innerWidth / 2;
	windowHalfY = window.innerHeight / 2;

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize( window.innerWidth, window.innerHeight );

}

function animate(){
	requestAnimationFrame( animate );
	render();
}

function render() {

	

	camera.position.x = 0;
	camera.position.y = -250;
	camera.position.z = 80;

	// mesh.rotation.x = inclinacionX;
	// mesh.rotation.y = inclinacionY;
	// mesh.rotation.z = inclinacionZ;

	mesh.rotation.x = (170+attitude.X)/-57.295779;
	mesh.rotation.y = (0+attitude.Y)/-57.295779;
	mesh.rotation.z = (20+attitude.z)/57.295779;;

	


/*	mesh.rotation.x = (180)/-57.295779;
	mesh.rotation.y = (0)/-57.295779;
	mesh.rotation.z = (20)/57.295779;*/

	//actualizarInclinacion();
	//sconsole.log(attitude.X,attitude.Y,attitude.z);

	camera.lookAt( scene.position );
	renderer.render( scene, camera );

}
