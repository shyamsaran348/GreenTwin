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
            // Using native fetch to ensure correct boundary handling for multipart/form-data
            // and avoiding Axios default header conflicts
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:8000/disease/analyze/${id}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    // Browser automatically sets Content-Type to multipart/form-data; boundary=...
                },
                body: formData
            });

            if (!response.ok) {
                if (response.status === 401) throw new Error("Unauthorized");
                throw new Error("Upload failed");
            }

            const data = await response.json();
            setLastAnalysis(data);
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
        { name: 'Health', value: healthScore > 0 ? healthScore : 100, color: healthScore < 50 ? '#f44336' : '#4CAF50' },
        { name: 'Stress', value: stressScore, color: '#f44336' }, // This part is tricky, stress adds to the "gap" in the pie or should be separate?
        // Actually, for a ring chart, "Health" is the filled part. The rest is "Lost Health" (Stress/Disease).
        // Let's simplify: Value is Health, Color depends on status.
    ];

    const healthColor = healthScore < 50 ? '#f44336' : (healthScore < 80 ? '#FF9800' : '#4CAF50');
    const isCritical = healthScore < 50;

    return (
        <div className="plant-detail-container">
            <header>
                <Link to="/dashboard">&larr; Back to Dashboard</Link>
                <h1>
                    {plant.name}
                    <span
                        className="species-tag"
                        style={{ backgroundColor: healthColor, color: 'black', fontWeight: 'bold' }}
                    >
                        {plant.species}
                    </span>
                </h1>
            </header>

            <div className="detail-grid">
                <div className="health-card" style={{ borderColor: isCritical ? '#f44336' : '#333', boxShadow: isCritical ? '0 0 15px rgba(244, 67, 54, 0.3)' : 'none' }}>
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
                        <p>Health Score: <strong style={{ color: healthColor, fontSize: '1.2em' }}>{healthScore != null ? Math.round(healthScore) : 'N/A'}</strong></p>
                        <div style={{ marginTop: '10px' }}>
                            <p style={{ marginBottom: '5px' }}>Water Stress: {(stressScore).toFixed(0)}%</p>
                            <div style={{ width: '100%', background: '#333', borderRadius: '10px', height: '10px', overflow: 'hidden' }}>
                                <div style={{ width: `${stressScore}%`, background: stressScore > 30 ? '#f44336' : '#2196F3', height: '100%', transition: 'width 0.5s ease' }}></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="analysis-card">
                    <h2>Disease Intelligence</h2>
                    {plant.species.toLowerCase().includes('tomato') ? (
                        <>
                            <form onSubmit={handleUpload}>
                                <div className="upload-box">
                                    <input type="file" onChange={handleFileChange} accept="image/*" />
                                </div>
                                <button type="submit" disabled={!file || analyzing}>
                                    {analyzing ? 'Analyzing...' : 'Analyze Leaf'}
                                </button>
                            </form>

                            {lastAnalysis && (
                                <div className="result-box" style={{ borderColor: isCritical ? '#f44336' : '#00ADB5', background: isCritical ? 'rgba(244, 67, 54, 0.1)' : 'rgba(0, 173, 181, 0.1)' }}>
                                    <h3 style={{ color: isCritical ? '#f44336' : '#00ADB5' }}>Analysis Result</h3>
                                    <p>Prediction: <strong>{lastAnalysis.disease}</strong></p>
                                    <p>Confidence: {(lastAnalysis.confidence * 100).toFixed(1)}%</p>
                                </div>
                            )}
                        </>
                    ) : (
                        <div style={{ textAlign: 'center', padding: '20px', color: '#888' }}>
                            <p style={{ fontSize: '30px', marginBottom: '10px' }}>🧪🚧</p>
                            <p><strong>Experimental Feature</strong></p>
                            <p>Disease Intelligence is currently optimized for <strong>Tomato</strong> plants only.</p>
                            <p style={{ fontSize: '0.9em', marginTop: '10px' }}>Support for <strong>{plant.species}</strong> is coming in v2.0!</p>
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

            <div className="care-card" style={{ borderLeft: isCritical ? '5px solid #f44336' : '5px solid #00ADB5' }}>
                {/* ... Care content ... */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                    <h2 style={{ marginBottom: 0, color: isCritical ? '#f44336' : 'white' }}>
                        {isCritical ? '🚨 Emergency Recovery Plan' : 'Care Tips & Schedule'}
                    </h2>
                    <button
                        onClick={async () => {
                            try {
                                await api.post(`/plants/${id}/water`);
                                alert("💧 Plant watered! Recovery process started.");
                                fetchPlant();
                            } catch (e) {
                                console.error(e);
                            }
                        }}
                        style={{ padding: '8px 15px', background: isCritical ? '#f44336' : '#00ADB5', border: 'none', borderRadius: '20px', color: 'white', cursor: 'pointer', fontWeight: 'bold', boxShadow: '0 4px 6px rgba(0,0,0,0.3)' }}
                    >
                        {isCritical ? '🚑 Apply Treatment' : '💧 Water Plant'}
                    </button>
                </div>

                {(plant.plant_state?.disease_risk_index > 0.3 && plant.plant_state?.water_stress > 0.3) && (
                    <div style={{ background: 'rgba(255, 0, 0, 0.2)', border: '1px solid red', padding: '10px', borderRadius: '8px', marginBottom: '15px', color: '#ffaaaa' }}>
                        ⚠️ <strong>Compound Stress Warning:</strong> High Disease Risk + Water Stress is causing rapid health decline (Synergistic Damage).
                    </div>
                )}

                <ul className="care-list">
                    {isCritical ? (
                        <>
                            <li>🛑 <strong>ISOLATE:</strong> Move plant away from others to prevent spread.</li>
                            <li>✂️ <strong>PRUNE:</strong> Remove infected leaves (like the one analyzed).</li>
                            <li>💧 <strong>HYDRATE:</strong> Water immediately but avoid wetting leaves.</li>
                            <li>🧪 <strong>TREAT:</strong> Apply organic fungicide (Neem Oil) every 7 days.</li>
                        </>
                    ) : (
                        <>
                            <li>💧 <strong>Water:</strong> Keep soil moist, water every 2-3 days.</li>
                            <li>☀️ <strong>Light:</strong> Needs full sun (6-8 hours daily).</li>
                            <li>💊 <strong>Fertilizer:</strong> Apply balanced fertilizer every 2 weeks.</li>
                            <li>📅 <strong>Next Reminder:</strong> Water tomorrow at 9:00 AM.</li>
                        </>
                    )}
                </ul>
            </div>

            {/* Disease History Gallery */}
            {plant.disease_records && plant.disease_records.length > 0 && (
                <div className="history-card" style={{ marginTop: '20px', background: '#222', padding: '20px', borderRadius: '15px' }}>
                    <h2 style={{ marginBottom: '15px' }}>🌿 Leaf Health History</h2>
                    <div style={{ display: 'flex', gap: '15px', overflowX: 'auto', paddingBottom: '10px' }}>
                        {plant.disease_records.slice().reverse().map((record) => (
                            <div key={record.id} style={{ minWidth: '150px', background: '#333', borderRadius: '10px', padding: '10px', textAlign: 'center' }}>
                                <img
                                    src={`http://localhost:8000/${record.image_path}`}
                                    alt="Leaf Analysis"
                                    style={{ width: '100%', height: '120px', objectFit: 'cover', borderRadius: '8px', marginBottom: '8px' }}
                                />
                                <p style={{ fontSize: '0.9em', fontWeight: 'bold', color: record.predicted_class.toLowerCase().includes('healthy') ? '#4CAF50' : '#f44336' }}>
                                    {record.predicted_class.replace(/Tomato___/g, '').replace(/_/g, ' ')}
                                </p>
                                <p style={{ fontSize: '0.8em', color: '#888' }}>
                                    {new Date(record.timestamp).toLocaleDateString()}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

        </div>
    );
};

export default PlantDetail;
