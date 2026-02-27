import { useState } from "react";

function CropPredictor() {
  const [city, setCity] = useState("");
  const [data, setData] = useState(null);

  const autoPredict = async () => {
    if (!city) {
      alert("Please enter a city!");
      return;
    }

    const res = await fetch(`http://localhost:8000/auto_predict?city=${city}`);
    const result = await res.json();

    if (result.error) {
      alert(result.error);
      return;
    }

    setData(result);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "auto", marginTop: "20px" }}>
      <h2>🌱 Auto Crop Predictor</h2>

      <input
        type="text"
        placeholder="Enter city name"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          borderRadius: "6px",
          marginBottom: "10px",
        }}
      />

      <button onClick={autoPredict}>Predict</button>

      {data && (
        <div style={{ marginTop: "20px" }}>
          <h3>Predicted Crop: {data.crop}</h3>

          <p>
            <strong>City:</strong> {data.city}
          </p>

          <p>
            <strong>Weather:</strong>
            {data.temperature}°C, {data.humidity}% humidity, {data.rainfall}mm
            rain
          </p>

          <p>
            <strong>Soil:</strong>N {data.N}, P {data.P}, K {data.K}, pH{" "}
            {data.ph}
          </p>

          <h3>Dish Recommendation:</h3>
          <p>
            <strong>{data.dish}</strong>
          </p>

          <p>
            <strong>Ingredients:</strong>
            {data.ingredients.join(", ")}
          </p>

          <h3>Nutrition:</h3>
          <pre style={{ background: "#eee", padding: "10px" }}>
            {JSON.stringify(data.nutrition, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default CropPredictor;
