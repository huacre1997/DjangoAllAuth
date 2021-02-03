


let alertMessage=(title,content,icon,url)=>{
  $.confirm({
    theme:"modern",
    icon:icon,
    title: title,
    content: content,
    buttons: {
        confirm: function () {
          location.href = url;

        },
     
       
    }
});


}
(() => {
    'use strict';
    
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');
    console.log(forms);
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach((form) => {
      form.addEventListener('submit', (event) => {
        if (!form.checkValidity()) {
          console.log("if");
          event.preventDefault();
          form.classList.add('was-validated');
          before_pass.addEventListener("keyup",()=>{
            console.log("keyup");
            form.classList.remove("was-validated")
        
            before_pass.classList.remove("is-invalid")
        
          })
          new_pass.addEventListener("keyup",()=>{
            form.classList.remove("was-validated")
        
            new_pass.classList.remove("is-invalid")
            new_pass_repeat.classList.remove("is-invalid")
        
          })
          new_pass_repeat.addEventListener("keyup",()=>{
            form.classList.remove("was-validated")
        
            new_pass_repeat.classList.remove("is-invalid")
            new_pass.classList.remove("is-invalid")
        
          })
        }
        else{
          console.log("else")
          event.preventDefault();

      let btn=document.getElementById("btn_change_password")
  let form = document.getElementById('form_change_password');
  let before_pass=document.getElementById("before_pass")
  let new_pass_repeat=document.getElementById("new_pass_repeat")
  let new_pass=document.getElementById("new_pass")
  let formData = new FormData(form)
  
  fetch(btn.dataset.url,{
  method: "POST",
    
  body: formData}).then(res=>res.json()).then(response=>{
    console.log(response);
    form.classList.remove("was-validated")

    if(response.response=="ok"){
      new_pass.value=""
      new_pass_repeat.value=""
      before_pass.value=""
    
    }else{
    if(response.error.before_pass){
      console.log("if");
      before_pass.classList.add("is-invalid")
      document.getElementById("invalid_before_pass").innerHTML=response.error.before_pass[0]
      form.classList.remove("was-validated")

    }else{
      console.log("else");
      if(response.error.__all__){
        
        new_pass_repeat.classList.add("is-invalid")
        document.getElementById("invalid_new_pass").innerHTML=response.error.__all__[0]
        new_pass.classList.add("is-invalid")
        document.getElementById("invalid_repeat_pass").innerHTML=response.error.__all__[0]
        form.classList.remove("was-validated")

      }
    }

      console.log("if");
      new_pass.value=""
      new_pass_repeat.value=""
      before_pass.value=""
    }
  })
        }
        before_pass.addEventListener("keyup",()=>{
          console.log("keyup");
          form.classList.remove("was-validated")
      
          before_pass.classList.remove("is-invalid")
      
        })
        new_pass.addEventListener("keyup",()=>{
          form.classList.remove("was-validated")
      
          new_pass.classList.remove("is-invalid")
          new_pass_repeat.classList.remove("is-invalid")
      
        })
        new_pass_repeat.addEventListener("keyup",()=>{
          form.classList.remove("was-validated")
      
          new_pass_repeat.classList.remove("is-invalid")
          new_pass.classList.remove("is-invalid")
      
        })
      }, false);
    });
  })();

  