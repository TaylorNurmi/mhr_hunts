function openForm() {
    document.getElementById("new_photo").style.display = "block";
}
function closeForm() {
    document.getElementById("new_photo").style.display = "none";
}

var apples = document.querySelectorAll(".this_div");
var oranges = document.querySelectorAll(".comments_button")
counter = 1
for (var i=0; i<apples.length; i++){
    oranges[i].setAttribute("id", `${counter}`)
    counter = counter + 1
    console.log("is this working?")
    console.log(oranges[i].id)
}

function ShowAndHide(){
var a =$(this).closest("div[.this_div]").prev().find(".this_div").val()
console.log(a)
}

function ShowAndHide(elem){
    var a = elem.parentNode.nextSibling;
    if(a.nextSibling.style.display == "none"){
        a.nextSibling.style.display = "block"
    }
    else{
        a.nextSibling.style.display = "none"
    }
}

function upLike(elem) {
    liked = document.getElementById(elem).style.color = "blue";
}

function ajaxpost (elem) {
    // (A) GET FORM DATA
    var form = document.getElementById(elem);
    var data = new FormData(form); 
    // (B) AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "add_like");
    // What to do when server responds
    xhr.onload = function () { console.log(this.response); };
    xhr.send(data);
    // (C) PREVENT HTML FORM SUBMIT
    return false;
}

function ajaxcomment (elem) {
    // (A) GET FORM DATA
    var form = document.getElementById(elem);
    var data = new FormData(form); 
    // (B) AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "addcomment");
    // What to do when server responds
    xhr.onload = function () { console.log(this.response); };
    xhr.send(data);
    // (C) PREVENT HTML FORM SUBMIT
    return false;
}
function showComment(id) {
    currentDiv = document.querySelector(".user_comment" + id);
    $("#evenbigger").load(location.href + " #evenbigger"); 
    redirect("#user_comment" + id);
}
function redirect(id) {
    $('#home').click(function(){
        $(document).scrollTop(100) // any value you need
        });
}
