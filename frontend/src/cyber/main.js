import React, { useState } from 'react';
import axios from 'axios';

const Main = () => {
    const [conversation, setConversation] = useState([]);
    const [input, setInput] = useState('');
    const [query, setQuery] = useState('');
    const [loading, setLoading] = useState(false);
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

        setLoading(true);
        setError(null);

        try {
            const response = await axios.post(`http://127.0.0.1:8000/${input}`, {
                input_sentence: query,
            });

            const taggedWords = response.data;

            setConversation((prev) => [
                ...prev,
                { sender: 'U', message: query, tableData: taggedWords },
            ]);

            setQuery('');
        } catch (err) {
            setError(err.message || 'No response from AI');
        } finally {
            setLoading(false);
        }
    };

    const handleClearChat = () => {
        setConversation([]);
    };

    return (
        <>
            <nav className="navbar">
                <ul>
                    <li><a href="/qna">Question and Answer</a></li>
                    <li><a href="/main">Annotate</a></li>
                    <li><button onClick={handleClearChat}>CLEAR CHAT</button></li>
                </ul>
            </nav>

            <div className="main-container">
                <div className="conversation-container">
                    {conversation.map((entry, index) => (
                        <div key={index} className="query-table-container">
                            <div className="user-query">
                                <strong>U:</strong> {entry.message}
                            </div>

                            <div className="table-container">
                                <table className="ai-output-table">
                                    <thead>
                                        <tr>
                                            <th>Word</th>
                                            <th>Tag</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {entry.tableData.map((wordTag, idx) => (
                                            <tr key={idx}>
                                                <td>{wordTag.q}</td>
                                                <td>{wordTag.a}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    ))}
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
