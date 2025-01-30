
document.getElementById('createAccountForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    let data = {};

    formData.forEach((value, key) => {
        data[key] = value;
    });

    console.log('Form Data Submitted:', data);
    alert('Account created successfully!');

    // Submit the form after logging the data
    this.submit(); 
});