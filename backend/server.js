const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const mongoose = require('mongoose');
const nodemailer = require('nodemailer');
const crypto = require('crypto');
const { spawn } = require('child_process');
const app = express();
const port = 8000; 

app.use(bodyParser.json());
app.use(cors());
<<<<<<< HEAD
const pythonExecutable = process.env.PYTHON_EXEC || 'C:\\Users\\Anand\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe';
const scriptBasePath = process.env.SCRIPT_PATH || 'E:\\cyber\\backend\\';
=======
const pythonExecutable = process.env.PYTHON_EXEC || 'python.exe path;
const scriptBasePath = process.env.SCRIPT_PATH || '';
>>>>>>> be933727ec0a4dbdd3dcc96575726b48eb50dcd0

mongoose.connect('mongodb+srv://dbname:<password>.wlaczyu.mongodb.net/cybersec', {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => {
    console.log('Connected to MongoDB Atlas');
}).catch(err => {
    console.error('Failed to connect to MongoDB Atlas', err);
});

const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    username: { type: String, unique: true },
    password: String,
    otp: String,
    otpExp: Date
});

const User = mongoose.model('User', userSchema);

const gen = nodemailer.createTransport({
    service: 'Gmail',
    auth: {
        user: '',
        pass: '' 
    }
});

app.post('/register', async (req, res) => {
    const { name, email, username, password } = req.body;

    try {
        const existingUser = await User.findOne({ username });
        if (existingUser) {
            return res.status(400).json({ message: 'Username already exists' });
        }
        const otp = crypto.randomInt(10001, 99998).toString();
        const otpExp = Date.now() + 10 * 60 * 1000;

        const hashedPassword = await bcrypt.hash(password, 10);
        const user = new User({
            // userId:UserId.toString(),   
            name,
            email,
            username,
            password: hashedPassword,
            otp,
            otpExp
        });

        await user.save();

        const mailOptions = {
            from: 'k',
            to: email,
            subject: 'Your OTP for registration is',
            text: `Your OTP is ${otp}. It is valid for 10 minutes`
        };

        gen.sendMail(mailOptions, (error, info) => {
            if (error) {
                return res.status(500).json({ message: 'Failed to send OTP', error });
            } else {
                console.log('Email sent: ' + info.response);
                return res.status(200).json({ message: 'OTP sent to your email. Please verify to complete registration.' });
            }
        });
    } catch (error) {
        res.status(400).json({ message: 'User registration failed', error });
    }
});

app.post('/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        const user = await User.findOne({ email });
        if (user && await bcrypt.compare(password, user.password)) {
            res.status(200).json({ message: 'Login successful' });
        } else {
            res.status(400).json({ message: 'Invalid credentials' });
        }
    } catch (error) {
        res.status(500).json({ message: 'An error occurred', error });
    }
});

const executePythonScript = (scriptName, args = [], callback) => {
    const scriptPath = `${scriptBasePath}${scriptName}`;
    const response = spawn(pythonExecutable, [scriptPath, ...args]);

    let dataFromPython = '';
    let errorOccurred = false;

    response.stdout.on('data', (data) => {
        dataFromPython += data.toString();
    });

    response.stderr.on('data', (data) => {
        console.error(`Error from Python script: ${data.toString()}`);
        if (!errorOccurred) {
            errorOccurred = true;
            callback({ error: `Error from Python script: ${data.toString()}` });
        }
    });

    response.on('close', (code) => {
        if (!errorOccurred) {
            try {
                const jsonData = JSON.parse(dataFromPython);
                console.log("Data received from Python script:", jsonData);
                callback(null, jsonData);
            } catch (error) {
                console.error('Error parsing JSON:', error);
                callback({ error: 'Internal Server Error: Error parsing JSON' });
            }
        }
    });

    response.on('error', (error) => {
        console.error('Error executing Python script:', error);
        if (!errorOccurred) {
            errorOccurred = true;
            callback({ error: 'Internal Server Error: Error executing Python script' });
        }
    });
};



// // app.post('/save-chat', async (req, res) => {
// //     const { userId, message, response } = req.body;

// //     try {
// //         const chat = new Chat({ userId, message, response });
// //         await chat.save();
// //         return res.status(200).json({ message: 'Chat saved successfully' });
// //     } catch (error) {
// //         return res.status(500).json({ error: 'Failed to save chat' });
// //     }
// // });

// app.get('/chat-history/:userId', async (req, res) => {
//     const { userId } = req.params;

//     try {
//         const chatHistory = await Chat.find({ userId }).sort({ timestamp: -1 });
//         return res.status(200).json(chatHistory);
//     } catch (error) {
//         return res.status(500).json({ error: 'Failed to retrieve chat history' });
//     }
// });


app.post('/knn', async (req, res) => {
    const { input_sentence } = req.body;
    if (!input_sentence) {
        return res.status(400).json({ error: 'Input sentence is required' });
    }
    console.log("Received input sentence:", input_sentence);
    
    executePythonScript('knn.py', [input_sentence], (error, data) => {
        if (error) return res.status(500).json(error);
        
        if (data) {
            return res.status(200).json(data);
        } else {
            return res.status(400).json({ error: 'No response from KNN model' });
        }
    });
});

app.post('/dt', async (req, res) => {
    const { input_sentence } = req.body;
    if (!input_sentence) {
        return res.status(400).json({ error: 'Input sentence is required' });
    }
    console.log("Received input sentence:", input_sentence);
    
    executePythonScript('dt.py', [input_sentence], (error, data) => {
        if (error) return res.status(500).json(error);
        
        if (data) {
            return res.status(200).json(data);
        } else {
            return res.status(400).json({ error: 'No response from KNN model' });
        }
    });
});

app.post('/lr', async (req, res) => {
    const { input_sentence } = req.body;
    if (!input_sentence) {
        return res.status(400).json({ error: 'Input sentence is required' });
    }
    console.log("Received input sentence:", input_sentence);
    
    executePythonScript('lr.py', [input_sentence], (error, data) => {
        if (error) return res.status(500).json(error);
        
        if (data) {
            return res.status(200).json(data);
        } else {
            return res.status(400).json({ error: 'No response from KNN model' });
        }
    });
});

app.post('/gb', async (req, res) => {
    const { input_sentence } = req.body;
    if (!input_sentence) {
        return res.status(400).json({ error: 'Input sentence is required' });
    }
    console.log("Received input sentence:", input_sentence);
    
    executePythonScript('gb.py', [input_sentence], (error, data) => {
        if (error) return res.status(500).json(error);
        
        if (data) {
            return res.status(200).json(data);
        } else {
            return res.status(400).json({ error: 'No response from KNN model' });
        }
    });
});

app.post('/rf', async (req, res) => {
    const { input_sentence } = req.body;
    if (!input_sentence) {
        return res.status(400).json({ error: 'Input sentence is required' });
    }
    console.log("Received input sentence:", input_sentence);
    
    executePythonScript('rf.py', [input_sentence], (error, data) => {
        if (error) return res.status(500).json(error);
        
        if (data) {
            return res.status(200).json(data);
        } else {
            return res.status(400).json({ error: 'No response from KNN model' });
        }
    });
});

app.post('/svm', async (req, res) => {
    const { input_sentence } = req.body;
    if (!input_sentence) {
        return res.status(400).json({ error: 'Input sentence is required' });
    }
    console.log("Received input sentence:", input_sentence);
    
    executePythonScript('svm.py', [input_sentence], (error, data) => {
        if (error) return res.status(500).json(error);
        
        if (data) {
            return res.status(200).json(data);
        } else {
            return res.status(400).json({ error: 'No response from KNN model' });
        }
    });
});

app.post('/news', async (req, res) => {
    console.log('Fetching news');
    executePythonScript('news.py', [], (error, data) => {
        if (error) {
            return res.status(500).json({ error: 'Failed to fetch news' });
        }
        res.json(data);
    });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});


