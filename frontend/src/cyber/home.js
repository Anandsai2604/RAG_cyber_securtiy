import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './front1.css'; // Add CSS file for styling the components

const Front1 = () => {
    const [newsData, setNewsData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.post('http://localhost:8080/news')
            .then(response => {
                setNewsData(response.data); 
                setLoading(false);  
            })
            .catch(error => {
                console.error('Error fetching news data:', error);
                setError('Failed to fetch news. Please try again later.');
                setLoading(false);  
            });
    }, []);

    return (
        <div className="front1-container">
            <nav className="navbar">
                <ul>
                    <li><Link to="/qna">Question and Answer</Link></li>
                    <li><Link to="/main">Annotate</Link></li>
                </ul>
            </nav>

            <div className="news-container">
                {loading ? (
                    <p>Loading news...</p>
                ) : error ? (
                    <p>{error}</p>
                ) : (
                    newsData.length > 0 ? (
                        newsData.map((newsItem, index) => (
                            <div key={index} className="news-item">
                                <h2>{newsItem.title}</h2>
                                {newsItem.image && <img src={newsItem.image} alt={newsItem.title} className="news-image" />}
                                <p>{newsItem.description}</p>
                                <a href={newsItem.url} target="_blank" rel="noopener noreferrer">Read more</a>
                            </div>
                        ))
                    ) : (
                        <p>No news available at the moment.</p>
                    )
                )}
            </div>
        </div>
    );
};

export default Front1;
