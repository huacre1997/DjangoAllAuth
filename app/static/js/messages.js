

let TopMessage=(title,icon,time=5000)=>{
    const Toast = Swal.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: time,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.addEventListener("mouseenter", Swal.stopTimer);
          toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
      });

      Toast.fire({
        icon: icon,
        title:title         
      });
}
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