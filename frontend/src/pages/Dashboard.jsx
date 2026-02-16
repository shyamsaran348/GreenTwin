import React, { useEffect, useState } from 'react';
import api from '../services/api';
import PlantCard from '../components/PlantCard';
import AddPlantModal from '../components/AddPlantModal';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
    const [plants, setPlants] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { logout, user } = useAuth();

    const [weather, setWeather] = useState(null);

    // Initial fetch
    useEffect(() => {
        fetchPlants();
        fetchWeather();
    }, []);

    const fetchWeather = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                try {
                    const { latitude, longitude } = position.coords;

                    // 1. Fetch Weather
                    const response = await api.get(`/weather/?lat=${latitude}&lon=${longitude}`);
                    setWeather(response.data);

                    // 2. Sync Location to Backend (For Auto-Pilot)
                    // We do this silently
                    api.post('/users/location', { latitude, longitude }).catch(err => console.error("Loc Sync Failed", err));

                } catch (error) {
                    console.error("Failed to fetch weather", error);
                }
            }, (error) => {
                console.error("Geolocation error", error);
                // Default to New York if denied
                fetchDefaultWeather();
            });
        } else {
            fetchDefaultWeather();
        }
    };

    const fetchDefaultWeather = async () => {
        try {
            // Default: New York
            const response = await api.get(`/weather/?lat=40.7128&lon=-74.0060`);
            setWeather(response.data);
        } catch (error) {
            console.error("Failed to fetch default weather", error);
        }
    }

    const fetchPlants = async () => {
        try {
            const response = await api.get('/plants/');
            setPlants(response.data);
        } catch (error) {
            console.error("Failed to fetch plants", error);
        }
    };

    const handlePlantAdded = (newPlant) => {
        setPlants([...plants, newPlant]);
    };

    const [gardenType, setGardenType] = useState('balcony');

    const getTheme = () => {
        switch (gardenType) {
            case 'rooftop': return 'linear-gradient(to bottom, #87CEEB, #e0f7fa)'; // Sky blue
            case 'backyard': return 'linear-gradient(to bottom, #2e7d32, #4caf50)'; // Green
            case 'indoor': return 'linear-gradient(to bottom, #3e2723, #5d4037)'; // Cozy warm
            default: return 'linear-gradient(to bottom, #1a1a1a, #000000)'; // Default dark (Balcony)
        }
    };

    return (
        <div className="dashboard-container" style={{ minHeight: '100vh', background: getTheme(), transition: 'background 0.5s ease' }}>
            <header className="dashboard-header" style={{ background: 'rgba(0,0,0,0.3)', backdropFilter: 'blur(10px)', width: '100%', padding: '20px', boxSizing: 'border-box', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <h1 style={{ color: 'white', margin: 0 }}>My Garden</h1>
                    <select
                        value={gardenType}
                        onChange={(e) => setGardenType(e.target.value)}
                        style={{ background: 'rgba(255,255,255,0.2)', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '5px', marginTop: '5px', cursor: 'pointer' }}
                    >
                        <option value="balcony">🏢 Balcony Garden</option>
                        <option value="rooftop">☁️ Rooftop Garden</option>
                        <option value="backyard">🏡 Backyard Garden</option>
                        <option value="indoor">🏠 Indoor Garden</option>
                    </select>

                    {weather && (
                        <div className="weather-widget" style={{ fontSize: '0.9rem', color: '#eee', display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px' }}>
                            <span>{weather.condition}</span>
                            <span style={{ fontSize: '1.2rem', color: 'white', fontWeight: 'bold' }}>{weather.temperature}°C</span>
                            {weather.temperature > 30 && <span style={{ color: '#ff6b6b', background: 'rgba(0,0,0,0.5)', padding: '2px 6px', borderRadius: '4px' }}>🔥 High Heat Warning</span>}
                        </div>
                    )}
                </div>
                <div className="actions" style={{ display: 'flex', gap: '10px' }}>
                    <button onClick={() => setIsModalOpen(true)} className="add-btn" style={{ background: '#4CAF50', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>+ Add Plant</button>
                    <button onClick={logout} className="logout-btn" style={{ background: 'rgba(255,255,255,0.1)', color: 'white', border: '1px solid rgba(255,255,255,0.2)', padding: '10px 20px', borderRadius: '8px', cursor: 'pointer' }}>Logout</button>
                </div>
            </header>

            <div className="plants-grid" style={{ padding: '20px' }}>
                {plants.length === 0 ? (
                    <div style={{ textAlign: 'center', marginTop: '50px', color: 'rgba(255,255,255,0.7)' }}>
                        <h2>Your garden is empty! 🌱</h2>
                        <p>Add your first plant to get started.</p>
                    </div>
                ) : (
                    plants.map(plant => (
                        <PlantCard key={plant.id} plant={plant} />
                    ))
                )}
            </div>

            <AddPlantModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onPlantAdded={handlePlantAdded}
            />
        </div>
    );
};

export default Dashboard;
