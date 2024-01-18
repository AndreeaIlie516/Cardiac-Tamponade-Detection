<script>

</script>
  
  <style>
    /* Add CSS styles here */
    .welcome-container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      text-align: center;
    }
  
    .welcome-button {
      /* Style for your button */
      padding: 10px 20px;
      margin-top: 20px;
      background-color: blue;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
  </style>
  
  <div class="welcome-container">
    <div>
      <h1>Welcome to Cardiac Tamponade Detection</h1>
      <button class="welcome-button" on:click={() => window.location.href='/upload'}>
        Upload a picture
      </button>
    </div>
  </div>
  