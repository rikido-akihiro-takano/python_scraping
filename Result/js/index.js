$(document).ready(function($){
	resizeMap();
	$(window).resize(function(){
		 resizeMap();
	});
});

function resizeMap() {
	var obj = document.getElementById("imgmap");
	var width_org = 574;
	setTimeout(function(){
		var width_current = obj.offsetWidth; 
		var r = width_current / width_org;
		var lis = document.getElementsByTagName("area");
		lis[0].coords = cal_new_coords(r,"463,44,35");
		lis[1].coords = cal_new_coords(r,"490,133,35");
		lis[2].coords = cal_new_coords(r,"368,143,35");
		lis[3].coords = cal_new_coords(r,"477,218,35");
		lis[4].coords = cal_new_coords(r,"477,218,35");
		lis[5].coords = cal_new_coords(r,"295,188,35");
		lis[6].coords = cal_new_coords(r,"461,298,35");
		lis[7].coords = cal_new_coords(r,"387,309,35");
		lis[8].coords = cal_new_coords(r,"219,220,35");
		lis[9].coords = cal_new_coords(r,"312,314,35");
		lis[10].coords = cal_new_coords(r,"171,293,35");
	 }, 300);
};

function cal_new_coords(r, old_coords){
	var tmp = old_coords.split(',');
	var x = r * tmp[0];
	var y = r * tmp[1];
	var z = r * tmp[2];
	return x + "," + y + "," + z;
}