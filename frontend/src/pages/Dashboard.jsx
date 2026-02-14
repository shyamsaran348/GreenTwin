import React, { useEffect, useState } from 'react';
import api from '../services/api';
import PlantCard from '../components/PlantCard';
import AddPlantModal from '../components/AddPlantModal';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
    const [plants, setPlants] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { logout, user } = useAuth();

    // Initial fetch
    useEffect(() => {
        fetchPlants();
    }, []);

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

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1>My Garden</h1>
                <div className="actions">
                    <button onClick={() => setIsModalOpen(true)} className="add-btn">+ Add Plant</button>
                    <button onClick={logout} className="logout-btn">Logout</button>
                </div>
            </header>

            <div className="plants-grid">
                {plants.map(plant => (
                    <PlantCard key={plant.id} plant={plant} />
                ))}
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
