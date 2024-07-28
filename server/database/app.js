const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const fetch = require('node-fetch');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(express.raw({ type: '*/*' })); // Asegurarse de que express.raw() se está utilizando para parsear el cuerpo de la solicitud

const reviews_data = JSON.parse(fs.readFileSync("data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("data/dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/", { 'dbName': 'dealershipsDB' });

const Review = require('./review');
const Dealership = require('./dealership');

try {
    Review.deleteMany({}).then(() => {
        Review.insertMany(reviews_data['reviews']);
    });
    Dealership.deleteMany({}).then(() => {
        Dealership.insertMany(dealerships_data['dealerships']);
    });
} catch (error) {
    console.error('Error fetching documents', error);
}

// Función para obtener el sentimiento usando la URL personalizada
const getSentiment = async (text) => {
    const response = await fetch(`https://sentianalyzer.1jv1vr3kppbk.us-east.codeengine.appdomain.cloud/analyze/${encodeURIComponent(text)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Host': 'sentianalyzer.1jv1vr3kppbk.us-east.codeengine.appdomain.cloud'
        },
    });

    if (!response.ok) {
        console.error(`Sentiment API error: ${response.statusText}`);
        return 'neutral'; // Devuelve 'neutral' en caso de error
    }

    const data = await response.json();
    console.log(`Sentiment API response: ${JSON.stringify(data)}`);  // Log for debugging
    return data.sentiment;
};

// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API");
});

// Express route to fetch all car models
app.get('/fetchCars', async (req, res) => {
    try {
        // Asegúrate de tener la lógica para obtener los modelos de autos
        const carModels = [
            { CarMake: 'Toyota', CarModel: 'Corolla' },
            { CarMake: 'Honda', CarModel: 'Civic' },
            { CarMake: 'Ford', CarModel: 'Focus' },
            // Añade más modelos según sea necesario
        ];
        res.json({ CarModels: carModels });
    } catch (error) {
        res.status(500).json({ error: 'Error fetching car models' });
    }
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
    try {
        const documents = await Review.find();
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    try {
        const documents = await Review.find({ dealership: req.params.id });
        res.json({ reviews: documents });
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
    try {
        const dealers = await Dealership.find();
        res.json(dealers);
    } catch (err) {
        res.status(500).send(err);
    }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
    try {
        const dealers = await Dealership.find({ state: req.params.state });
        res.json(dealers);
    } catch (err) {
        res.status(500).send(err);
    }
});

// Corregir la ruta para obtener un dealer por ID
app.get('/fetchDealer/:id', async (req, res) => {
    try {
      const id = req.params.id;
      const document = await Dealership.findOne({ id: id }); // Usar findOne con el campo id
      if (!document) {
        return res.status(404).json({ error: 'Dealer not found' });
      }
      res.json(document);
    } catch (error) {
      res.status(500).json({ error: error.message + ' Error fetching documents' });
    }
  });

// Express route to insert review
app.post('/insert_review', async (req, res) => {
    try {
        const data = JSON.parse(req.body);
        const documents = await Review.find().sort({ id: -1 });
        let new_id = documents.length > 0 ? documents[0].id + 1 : 1; // Manejar el caso cuando no hay documentos

        // Obtener el sentimiento usando la URL personalizada
        const sentiment = await getSentiment(data.review);

        const review = new Review({
            id: new_id,
            name: data.name,
            dealership: data.dealership,
            review: data.review,
            purchase: data.purchase,
            purchase_date: data.purchase_date,
            car_make: data.car_make,
            car_model: data.car_model,
            car_year: data.car_year,
            sentiment: sentiment, // Asegúrate de que este campo se está incluyendo
            sentiment_raw: JSON.stringify(data) // Agregar la respuesta completa de sentimiento como verificación
        });

        const savedReview = await review.save();
        res.json(savedReview);
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: 'Error inserting review' });
    }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
    try {
        const id = req.params.id;
        const document = await Dealership.findById(id); // Usar findById para buscar por ID
        if (!document) {
            return res.status(404).json({ error: 'Dealer not found' });
        }
        res.json(document);
    } catch (error) {
        res.status(500).json({ error: error.message + ' Error fetching documents' });
    }
});

// Start the Express server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
