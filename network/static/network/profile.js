document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.texed').forEach(element => element.style.display='none');
        if(document.querySelector('button[name="follow"]') != null){
        document.querySelector('button[name="follow"]').addEventListener('click', function(){
            fs = this.innerHTML;
            id = this.id
            var k = true
            if( fs == 'Unfollow'){
                k = false;
            }
            fetch('/follow', {
              method: 'POST',
              body: JSON.stringify({
                  stat : k,
                  usid :id,
              })
            })
            .then(response => response.json())
            .then(result => {
                 value = result["is_follow"];
                 fg = result["fg"];
                 fr = result["fr"];
                 console.log(fg);
                 console.log(fr);
                 console.log(value);
                 if(value == true){
                    this.className = "btn btn-danger";
                    this.innerHTML = "Unfollow";
                    document.getElementById('follno1').innerHTML= fr;
                    document.getElementById('follno2').innerHTML= fg;
                 }
                 else{
                    this.className = "btn btn-success";
                    this.innerHTML = "Follow";
                    document.getElementById('follno1').innerHTML= fr;
                    document.getElementById('follno2').innerHTML= fg;
                 }
            })
        })}
        document.querySelectorAll('.likeu1').forEach(element => element.addEventListener('click', change_like));

        document.querySelectorAll('button[name="edit"]').forEach(element => element.addEventListener('click', edit_post));
})

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