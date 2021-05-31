document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".editpost").forEach(item => {
        item.addEventListener("click", () => editpost(item.dataset.postid));
    });

    document.querySelectorAll(".likebtn").forEach(item => {
        fetch('/isliked', {
            method: 'POST',
            body: JSON.stringify({
                postid: item.dataset.postid
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.liked === true) {
                item.src = "static/network/heartred.png";
            }else{
                item.src = "static/network/heart.png";
            }
            //console.log(item.src);
        })
        item.addEventListener("click", () => like(item.dataset.postid));
    });
})

function get_like_count(postid) {
    fetch('/getlikecount', {
        method: 'POST',
        body: JSON.stringify({
            postid: postid
        })
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById(`${postid}`).querySelector(".likecount").innerHTML = result.likecount;
    })
}

function like(postid) {
    let likebuttonparent = document.getElementById(`${postid}`);
    let likebutton = likebuttonparent.querySelector(".likebtn");
    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            postid: postid
        })
    })
    .then(response => response.json())
    .then(result => {
        // console.log(likebutton);
        if (result.liked === 1){
            likebutton.src = "static/network/heartred.png";
        }else{
            likebutton.src = "static/network/heart.png";
        }
        get_like_count(postid);
    })
}

function editpost(postid) {
    let post = document.getElementById(`${postid}`);
    let message = post.querySelector(".message");
    let editarea = post.querySelector(".editposttext");
    let editbutton = post.querySelector(".editpost");
    let text = message.innerHTML;
    let savebutton = post.querySelector(".saveedit");
    editbutton.style.display = "none";
    message.style.display = "none";
    editarea.style.display = "block";
    editarea.querySelector(".edittextarea").innerHTML = text;
    savebutton.addEventListener("click", () => saveedittedpost(postid));
    //console.log(message);
}

function saveedittedpost(postid) {
    let post = document.getElementById(`${postid}`);
    let editarea = post.querySelector(".editposttext");
    let userid = editarea.querySelector(".saveedit").dataset.userid;
    let newtext = editarea.querySelector(".edittextarea").value;
    let editbutton = post.querySelector(".editpost");
    let message = post.querySelector(".message");
    //console.log(newtext);
    fetch('/editpost', {
        method: 'POST',
        body: JSON.stringify({
            userid: userid,
            postid: postid,
            posttext: newtext
        })
    })
    // .then(response => response.json())
    // .then(result => {
    //     // Print result
    //     console.log(result.message);
    // })
    .then(response => {
        if (response.ok) {
            editarea.style.display = "none";
            editbutton.style.display = "block";
            message.style.display = "block";
            message.innerHTML = newtext;
        }
    });
}