import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png";
import neutral_icon from "../assets/neutral.png";
import negative_icon from "../assets/negative.png";
import review_icon from "../assets/reviewbutton.png";
import Header from '../Header/Header';

const Dealer = () => {
  const [dealer, setDealer] = useState({});
  const [reviews, setReviews] = useState([]);
  const [unreviewed, setUnreviewed] = useState(false);
  const [postReview, setPostReview] = useState(<></>);

  let params = useParams();
  let id = params.id;
  let dealer_url = `http://localhost:3030/fetchDealer/${id}`;
  let reviews_url = `http://localhost:3030/fetchReviews/dealer/${id}`;
  let post_review = `/postreview/${id}`;

  const get_dealer = async () => {
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    
    if (res.ok) {
      setDealer(retobj);
    }
  };

  const get_reviews = async () => {
    const res = await fetch(reviews_url, {
      method: "GET"
    });
    const retobj = await res.json();

    if (res.ok) {
      console.log(`Reviews received: ${JSON.stringify(retobj.reviews)}`);  // Log for debugging
      if (retobj.reviews.length > 0) {
        setReviews(retobj.reviews);
      } else {
        setUnreviewed(true);
      }
    }
  };

  const senti_icon = (sentiment) => {
    console.log(`Sentiment received: ${sentiment}`);  // Log for debugging
    if (sentiment === "positive") return positive_icon;
    if (sentiment === "negative") return negative_icon;
    return neutral_icon;
  };

  useEffect(() => {
    get_dealer();
    get_reviews();
    if (sessionStorage.getItem("username")) {
      setPostReview(<a href={post_review}><img src={review_icon} style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }} alt='Post Review'/></a>);
    }
  }, []);

  return (
    <div style={{ margin: "20px" }}>
      <Header/>
      <div style={{ marginTop: "10px" }}>
        <h1 style={{ color: "grey" }}>{dealer.full_name}{postReview}</h1>
        <h4 style={{ color: "grey" }}>{dealer.city}, {dealer.address}, Zip - {dealer.zip}, {dealer.state}</h4>
      </div>
      <div className="reviews_panel">
        {reviews.length === 0 && !unreviewed ? (
          <text>Loading Reviews....</text>
        ) : unreviewed ? (
          <div>No reviews yet!</div>
        ) : (
          reviews.map(review => (
            <div className='review_panel' key={review.id}>
              <img src={senti_icon(review.sentiment)} className="emotion_icon" alt={`Sentiment: ${review.sentiment}`} />
              <div className='review'>{review.review}</div>
              <div className="reviewer">{review.name} {review.car_make} {review.car_model} {review.car_year}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dealer;
