document.addEventListener("DOMContentLoaded", () => {
    const followbutton = document.querySelector("#follow");
    followbutton.addEventListener("click", () => follow(document.querySelector("#follow").dataset.userid));
    isfollowing();
})

function isfollowing() {
    fetch('/isfollowing', {
        method: 'POST',
        body: JSON.stringify({
            userid: document.querySelector("#follow").dataset.userid
        })
    })
    .then(response => response.json())
    .then(result => {
        //console.log(result.buttontext)
        document.querySelector("#follow").innerHTML = result.buttontext;
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

function follow(userid) {
    // console.log(userid);
    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify({
            userid: userid
        })
    })
    .then(response => {
        if (response.ok) {
            isfollowing();
            updateFollowerCount();
        }
    });
}

function updateFollowerCount() {
    fetch('/updatefollowcount', {
        method: 'POST',
        body: JSON.stringify({
            userid: document.querySelector("#follow").dataset.userid
        })
    })
    .then(response => response.json())
    .then(result => {
        //console.log(result.buttontext)
        document.querySelector("#following").innerHTML = "Following: " + result.following;
        document.querySelector("#followers").innerHTML = "Followers: " + result.followers;
    })
    .catch(error => {
        console.log('Error:', error);
    });
}