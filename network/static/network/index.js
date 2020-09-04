document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('textarea[name="postc"]') != null){
    document.querySelector('textarea[name="postc"]').value = '';}
    document.querySelectorAll('.texed').forEach(element => element.style.display='none');
    document.querySelectorAll('.likeu1').forEach(element => element.addEventListener('click', change_like));
    document.querySelectorAll('button[name="edit"]').forEach(element => element.addEventListener('click', edit_post));
})

/*
function change_like(){
    post_id = document.querySelector('span[name="likeu1"]').id;
    console.log(post_id)
    fetch('/likes', {
      method: 'POST',
      body: JSON.stringify({
          post_id = post_id,
      })
    })
    .then(response => response.json())
    .then(result => {
        value = result["is_liked"];
        console.log(value)
        if (value == 'true'){
            document.querySelector('span[name="likeu1"]').style.color= 'red';
        }
        else{
            document.querySelector('span[name="likeu1"]').style.color= 'grey';
        }
    })
}
*/

function change_like(){
    post_id = this.id
    console.log(post_id)
    fetch('/likes', {
      method: 'POST',
      body: JSON.stringify({
          post_id : post_id,
      })
    })
    .then(response => response.json())
    .then(result => {
        value = result["is_liked"];
        cou = result["no_likes"];
        console.log(cou);
        console.log(value);
        console.log(value == true);
        console.log(this);
        if (value == true){
            this.style.color = 'red';
            document.getElementById(`${post_id}l`).innerHTML = cou;
            console.log('red');
        }
        else{
            this.style.color = 'grey';
            document.getElementById(`${post_id}l`).innerHTML = cou;
            console.log('grey');
        }
    })
}

function edit_post(){
    post_id = this.id.slice(0,-1);
    this.style.display = 'none';
    console.log(post_id);
    cont = document.getElementById(`${post_id}c`).innerHTML;
    console.log(cont);
    document.getElementById(`${post_id}c`).style.display = 'none';
    document.getElementById(`${post_id}e`).style.display = 'block';
    document.getElementById(`${post_id}e1`).value = cont;
    document.getElementById(`${post_id}s`).addEventListener('click', function(event){
        event.preventDefault();
        con = document.getElementById(`${post_id}e1`).value;
        console.log(con);
        fetch('/edit', {
          method: 'POST',
          body: JSON.stringify({
              content: con,
              post_id: post_id
          })
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById(`${post_id}e`).style.display = 'none';
            document.getElementById(`${post_id}c`).style.display = 'block';
            this.style.display = 'block';
            document.getElementById(`${post_id}c`).innerHTML = con;
        })
    })

}

