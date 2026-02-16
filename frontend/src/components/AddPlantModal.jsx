import React, { useState } from 'react';
import api from '../services/api';

const AddPlantModal = ({ isOpen, onClose, onPlantAdded }) => {
    const [name, setName] = useState('');
    const [species, setSpecies] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const formData = new FormData();
        formData.append('name', name);
        formData.append('species', species);
        if (file) {
            formData.append('file', file);
        } else {
            // Backend requires file, so maybe alert user? 
            // Or backend should handle optional file. 
            // The user requested "image should be included", so let's make it required.
            alert("Please upload an image of your plant!");
            setLoading(false);
            return;
        }

        try {
            const response = await api.post('/plants/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            onPlantAdded(response.data);
            setName('');
            setSpecies('');
            setFile(null);
            onClose();
        } catch (error) {
            console.error("Failed to add plant", error);
            alert("Failed to add plant. See console.");
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
                            <option value="Apple">Apple</option>
                            <option value="Blueberry">Blueberry</option>
                            <option value="Cherry">Cherry</option>
                            <option value="Corn">Corn (Maize)</option>
                            <option value="Grape">Grape</option>
                            <option value="Orange">Orange</option>
                            <option value="Peach">Peach</option>
                            <option value="Pepper">Pepper, Bell</option>
                            <option value="Potato">Potato</option>
                            <option value="Raspberry">Raspberry</option>
                            <option value="Soybean">Soybean</option>
                            <option value="Squash">Squash</option>
                            <option value="Strawberry">Strawberry</option>
                            <option value="Tomato">Tomato</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label>Plant Photo (Required for Health Check)</label>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={(e) => setFile(e.target.files[0])}
                            required
                        />
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
