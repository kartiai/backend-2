const email = document.getElementById('username')
const password = document.getElementById('password')

const form = document.getElementById('form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const response = await fetch('/login', {
    method: 'POST',
    body: formData,
  }).then((response) =>
  {
    console.log(response.json());
    if (responseData.code == '200') {
      // Redirect to success page
      console.log("redirecting")
      window.location.href = '/';
    } else {
      console.log('fail');
    }
  }
  )
});





form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  const response = await fetch('/submit-form', {
    method: 'POST',
    body: formData
  });

  const responseData = await response.json();


  if (responseData.code == '400') {
    // Redirect to success page
    console.log('ok');
  } else {
    // Redirect to error page
    console.log('baf');
  }
});