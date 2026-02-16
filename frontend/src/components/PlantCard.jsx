import React from 'react';
import { Link } from 'react-router-dom';

const PlantCard = ({ plant }) => {
    return (
        <div className="plant-card">
            {/* Placeholder image logic */}
            <div className="plant-image">
                <img
                    src={plant.image_path ? `http://localhost:8000/${plant.image_path}` : "https://placehold.co/400x300/2a9d8f/ffffff?text=GreenTwin"}
                    alt={plant.name}
                    style={{ width: '100%', height: '200px', objectFit: 'cover' }}
                    onError={(e) => e.target.src = "https://placehold.co/400x300/2a9d8f/ffffff?text=GreenTwin"}
                />
            </div>
            <div className="plant-info">
                <h3>{plant.name}</h3>
                <p className="species">{plant.species}</p>
                <Link to={`/plants/${plant.id}`} className="view-btn">View Details</Link>
            </div>
        </div>
    );
};

export default PlantCard;
