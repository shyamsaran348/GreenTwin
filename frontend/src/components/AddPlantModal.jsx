import React, { useState } from 'react';
import api from '../services/api';

const AddPlantModal = ({ isOpen, onClose, onPlantAdded }) => {
    const [name, setName] = useState('');
    const [species, setSpecies] = useState('');
    const [loading, setLoading] = useState(false);

    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await api.post('/plants/', { name, species });
            onPlantAdded(response.data);
            setName('');
            setSpecies('');
            onClose();
        } catch (error) {
            console.error("Failed to add plant", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal">
                <button className="close-btn" onClick={onClose}>&times;</button>
                <h2>Add New Plant</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Plant Name</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Species / Type</label>
                        <select
                            value={species}
                            onChange={(e) => setSpecies(e.target.value)}
                            required
                        >
                            <option value="">Select Species</option>
                            <option value="Tomato">Tomato</option>
                            <option value="Potato">Potato</option>
                            <option value="Pepper">Pepper</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <button type="submit" disabled={loading}>
                        {loading ? 'Adding...' : 'Add Plant'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AddPlantModal;
