import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './main.css';

const Main = () => {
    const [conversation, setConversation] = useState([]);
    const [AnsData, setAnsData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [input, setInput] = useState('');
    const [query, setQuery] = useState('');
    const [error, setError] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!input) {
            alert('Please select a model');
            return;
        }
        if (!query) {
            alert('Please enter a query.');
            return;
        }

        console.log("Query:", query);

        setLoading(true);
        setAnsData([]);
        setError(null);

        try {
            const response = await axios.post(`http://127.0.0.1:8000/${input}`, {
                input_sentence: query,  // Send query as input_sentence
            });
            console.log(response.data);
            const aiResponse = response.data[0]?.a || 'No response from AI';
            setConversation((prev) => [
                ...prev,
                { sender: 'U', message: query },
                { sender: 'AI', message: aiResponse },
            ]);

            // Store AI response data to populate a table
            setAnsData((prev) => [
                ...prev,
                { model: input, query: query, answer: aiResponse }
            ]);

            // Clear the query after submission
            setQuery('');
        } catch (err) {
            setError(err.message || 'No response from AI');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <nav className="navbar">
                <ul>
                    <li><Link to="/qna">Question and Answer</Link></li>
                    <li><Link to="/main">Annotate</Link></li>
                </ul>
            </nav>

            <div className="main-container">
                <div className="conversation-container">
                    {conversation.map((msg, index) => (
                        <div key={index} className={`message ${msg.sender === 'U' ? 'user' : 'ai'}`}>
                            <span>
                                <strong>{msg.sender === 'U' ? 'U:' : 'AI:'}</strong> {msg.message}
                            </span>
                        </div>
                    ))}
                    {loading && <p className="loading-text">Loading...</p>}
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                </div>

                {/* Table for AI Output */}
                <div className="table-container">
                    {AnsData.length > 0 && (
                        <table className="ai-output-table">
                            <thead>
                                <tr>
                                    <th>Model</th>
                                    <th>Query</th>
                                    <th>Answer</th>
                                </tr>
                            </thead>
                            <tbody>
                                {AnsData.map((data, index) => (
                                    <tr key={index}>
                                        <td>{data.model}</td>
                                        <td>{data.query}</td>
                                        <td>{data.answer}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>

                <div className="input-container">
                    <form onSubmit={handleSearch}>
                        <select value={input} onChange={(e) => setInput(e.target.value)} className="dropdown">
                            <option value="">Select Model</option>
                            <option value="rf">Random Forest</option>
                            <option value="dt">Decision Tree</option>
                            <option value="lr">Logistic Regression</option>
                            <option value="svm">SVM</option>
                            <option value="gb">LightGBM</option>
                        </select>
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Type your query"
                            className="query-input"
                        />
                        <button type="submit" className="send-button">Send</button>
                    </form>
                </div>
            </div>
        </>
    );
};

export default Main;
