import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './front1.css';

const Front1 = () => {
    const [newsData, setNewsData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.post('http://127.0.0.1:8000/news')
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
                                <div className="news-content">
                                    {newsItem.image && (
                                        <div className="news-image-wrapper">
                                            <img src={newsItem.image} alt={newsItem.header} className="news-image" />
                                        </div>
                                    )}
                                    <div className="news-text">
                                        <h2 className="news-title">
                                            <a href={newsItem.link} target="_blank" rel="noopener noreferrer">
                                                {newsItem.header}
                                            </a>
                                        </h2>
                                        <p className="news-description">{newsItem.para}</p>
                                        <a href={newsItem.link} target="_blank" rel="noopener noreferrer" className="read-more">
                                            Read more
                                        </a>
                                    </div>
                                </div>
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
