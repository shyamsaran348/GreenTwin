import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend, LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';

const PlantDetail = () => {
    const { id } = useParams();
    const [plant, setPlant] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [file, setFile] = useState(null);
    const [lastAnalysis, setLastAnalysis] = useState(null);

    useEffect(() => {
        fetchPlant();
    }, [id]);

    const fetchPlant = async () => {
        try {
            const response = await api.get(`/plants/${id}`);
            setPlant(response.data);
        } catch (error) {
            console.error("Failed to fetch plant", error);
        }
    };

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!file) return;

        setAnalyzing(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post(`/disease/analyze/${id}`, formData);
            setLastAnalysis(response.data);
            fetchPlant(); // Refresh state
        } catch (error) {
            console.error("Analysis failed", error);
        } finally {
            setAnalyzing(false);
        }
    };

    if (!plant) return <div>Loading...</div>;

    // Data for charts
    // In a real app complexity, these would be historical data
    // Assuming plant.plant_state exists (backend needs to return it, Schema Update needed?)
    // Wait, PlantOut schema says "We will add plant_state later".
    // I need to update PlantOut schema to include plant_state!

    const healthScore = plant.plant_state?.health_score || 0;
    const stressScore = plant.plant_state?.water_stress ? plant.plant_state.water_stress * 100 : 0;

    const healthData = [
        { name: 'Health', value: healthScore > 0 ? healthScore : 100, color: '#4CAF50' },
        { name: 'Stress', value: stressScore, color: '#f44336' },
    ];

    return (
        <div className="plant-detail-container">
            <header>
                <Link to="/dashboard">&larr; Back to Dashboard</Link>
                <h1>{plant.name} <span className="species-tag">{plant.species}</span></h1>
            </header>

            <div className="detail-grid">
                <div className="health-card">
                    <h2>Health Status</h2>
                    <div style={{ width: '100%', height: 300 }}>
                        <ResponsiveContainer>
                            <PieChart>
                                <Pie
                                    data={healthData}
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {healthData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="scores">
                        <p>Health Score: <strong>{plant.plant_state?.health_score != null ? plant.plant_state.health_score : 'N/A'}</strong></p>
                        <p>Water Stress: {plant.plant_state?.water_stress != null ? (plant.plant_state.water_stress * 100).toFixed(0) : 0}%</p>
                    </div>
                </div>

                <div className="analysis-card">
                    <h2>Disease Intelligence</h2>
                    <form onSubmit={handleUpload}>
                        <div className="upload-box">
                            <input type="file" onChange={handleFileChange} accept="image/*" />
                        </div>
                        <button type="submit" disabled={!file || analyzing}>
                            {analyzing ? 'Analyzing...' : 'Analyze Leaf'}
                        </button>
                    </form>

                    {lastAnalysis && (
                        <div className="result-box">
                            <h3>Analysis Result</h3>
                            <p>Prediction: <strong>{lastAnalysis.disease}</strong></p>
                            <p>Confidence: {(lastAnalysis.confidence * 100).toFixed(1)}%</p>
                        </div>
                    )}
                </div>
            </div>

            <div className="timeline-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                    <h2 style={{ marginBottom: 0 }}>Growth Timeline</h2>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="number"
                            placeholder="Height (cm)"
                            style={{ padding: '5px', borderRadius: '5px', border: '1px solid #444', background: '#333', color: 'white', width: '100px' }}
                            id="heightInput"
                        />
                        <button
                            onClick={async () => {
                                const height = document.getElementById('heightInput').value;
                                if (!height) return;
                                try {
                                    await api.post(`/plants/${id}/log`, { height: parseFloat(height) });
                                    document.getElementById('heightInput').value = '';
                                    fetchPlant();
                                } catch (e) {
                                    console.error(e);
                                }
                            }}
                            style={{ padding: '5px 10px', background: '#00ADB5', border: 'none', borderRadius: '5px', color: 'black', cursor: 'pointer', fontWeight: 'bold' }}
                        >
                            Log
                        </button>
                    </div>
                </div>

                <div style={{ width: '100%', height: 300 }}>
                    <ResponsiveContainer>
                        <LineChart data={plant.logs && plant.logs.length > 0 ? plant.logs.map(log => ({
                            date: new Date(log.recorded_at).toLocaleDateString(),
                            height: log.height
                        })) : []}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                            <XAxis dataKey="date" stroke="#aaa" />
                            <YAxis stroke="#aaa" />
                            <Tooltip contentStyle={{ backgroundColor: '#333', borderColor: '#444' }} />
                            <Legend />
                            <Line type="monotone" dataKey="height" stroke="#00ADB5" strokeWidth={3} name="Height (cm)" />
                        </LineChart>
                    </ResponsiveContainer>
                    {(!plant.logs || plant.logs.length === 0) && (
                        <p style={{ textAlign: 'center', color: '#666', fontStyle: 'italic', marginTop: '-150px' }}>
                            No growth data yet. Add your first log above! 📈
                        </p>
                    )}
                </div>
            </div>

            <div className="care-card">
                <h2>Care Tips & Schedule</h2>
                <ul className="care-list">
                    <li>💧 <strong>Water:</strong> Keep soil moist, water every 2-3 days.</li>
                    <li>☀️ <strong>Light:</strong> Needs full sun (6-8 hours daily).</li>
                    <li>💊 <strong>Fertilizer:</strong> Apply balanced fertilizer every 2 weeks.</li>
                    <li>📅 <strong>Next Reminder:</strong> Water tomorrow at 9:00 AM.</li>
                </ul>
            </div>
        </div>
    );
};

export default PlantDetail;
