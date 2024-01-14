<script lang="ts">
  interface DataReceived {
    confidence?: number; 
    predicted_label?: string;
  };

  interface DataSent {
    image_path: string;
  };

  const url = "http://localhost:5000/getPredictionOutput";
  let prediction: DataReceived = {};
  let dataToSend: DataSent | undefined;
  let file: File | null = null; 
  let imagePath: string | null = null;
  let imageSrc: string | undefined;

  function handleFileEvent(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      file = input.files[0];
      imagePath = './images/' + file.name;
      dataToSend = { image_path: imagePath };
    }
  }

  async function sendPostRequest() {
    if (!dataToSend) {
      console.log("No data to send");
      return;
    }
    try {
      const response = await fetch(url, {
        method: 'POST', 
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      prediction = await response.json();
      console.log('Response:', prediction);
    } catch (error) {
      console.error('Error posting image path:', error);
    }
  }
</script>

<div>
  <input type="file" on:change={handleFileEvent}>
  {#if file} 
    <p>File selected: {file.name}</p>
    <button on:click={sendPostRequest}>Scan picture</button>
  {/if}
  {#if prediction.predicted_label}
    <p>Prediction: {prediction.predicted_label}</p>
    <p>Confidence: {prediction.confidence?.toFixed(2)}%</p>
  {/if}
</div>


<style>
  div {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }

  input[type="file"] {
    margin: 20px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    transition: border-color 0.3s;
  }

  input[type="file"]:hover,
  input[type="file"]:focus {
    border-color: #007bff;
  }

  button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  button:hover {
    background-color: #0056b3;
  }

  p {
    margin: 10px 0;
    font-size: 1.1rem;
  }
</style>
