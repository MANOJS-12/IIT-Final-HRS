import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { User, Activity, Brain, Users, Sun, ClipboardList, Shield, Briefcase, Network, Sparkles } from 'lucide-react';
import ForceGraph2D from 'react-force-graph-2d';
import './index.css';

// Mock users for demo
const DEMO_USERS = [
    { id: 'U0', name: 'User 0', desc: 'Corporate, Female, US' },
    { id: 'U1', name: 'User 1', desc: 'Corporate, Female, US' },
    { id: 'U2', name: 'User 2', desc: 'Corporate, Female, US' },
    { id: 'U7', name: 'User 7', desc: 'Corporate, Female, Australia' },
];

function App() {
    const [mode, setMode] = useState('profile'); // 'profile', 'assessment'
    const [selectedUser, setSelectedUser] = useState(null);
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);

    // Form State
    const [formData, setFormData] = useState({
        growing_stress: 'No',
        mood_swings: 'Low',
        social_weakness: 'No',
        coping_struggles: 'No',
        work_interest: 'Yes'
    });

    const handleUserSelect = async (user) => {
        setSelectedUser(user);
        setLoading(true);
        setRecommendations([]);

        try {
            const response = await axios.post('http://localhost:8000/recommend', {
                user_id: user.id,
                strategy: 'hybrid'
            });
            setRecommendations(response.data);
        } catch (error) {
            console.error("Error fetching recommendations:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setRecommendations([]);
        setSelectedUser(null);

        try {
            const response = await axios.post('http://localhost:8000/recommend', {
                ...formData,
                strategy: 'hybrid'
            });
            setRecommendations(response.data);
        } catch (error) {
            console.error("Error fetching recommendations:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <header style={{ marginBottom: '3rem', textAlign: 'center' }}>
                <motion.h1
                    initial={{ y: -50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    style={{ fontSize: '3rem', marginBottom: '1rem' }}
                >
                    Mental Health <span style={{ color: '#627d98' }}>Companion</span>
                </motion.h1>

                <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginTop: '2rem', flexWrap: 'wrap' }}>
                    <button
                        className={`btn ${mode === 'profile' ? 'active' : ''}`}
                        onClick={() => { setMode('profile'); setRecommendations([]); }}
                        style={{
                            background: mode === 'profile' ? '#627d98' : 'white',
                            color: mode === 'profile' ? 'white' : '#627d98',
                            padding: '0.8rem 2rem', border: 'none', borderRadius: '2rem', cursor: 'pointer', fontWeight: 'bold'
                        }}
                    >
                        Demo Profiles
                    </button>
                    <button
                        className={`btn ${mode === 'assessment' ? 'active' : ''}`}
                        onClick={() => { setMode('assessment'); setRecommendations([]); }}
                        style={{
                            background: mode === 'assessment' ? '#627d98' : 'white',
                            color: mode === 'assessment' ? 'white' : '#627d98',
                            padding: '0.8rem 2rem', border: 'none', borderRadius: '2rem', cursor: 'pointer', fontWeight: 'bold'
                        }}
                    >
                        Real-time Assessment
                    </button>
                </div>
            </header>

            {/* MODE: PROFILES */}
            {mode === 'profile' && (
                <div className="grid-cards" style={{ marginBottom: '4rem' }}>
                    {DEMO_USERS.map((user) => {
                        const isSelected = selectedUser?.id === user.id;
                        return (
                            <motion.div
                                key={user.id}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => handleUserSelect(user)}
                                className="glass-panel"
                                style={{
                                    padding: '1.5rem',
                                    cursor: 'pointer',
                                    textAlign: 'center',
                                    background: isSelected ? 'rgba(255, 255, 255, 0.95)' : 'rgba(255, 255, 255, 0.6)',
                                    border: isSelected ? '2px solid #627d98' : '1px solid transparent',
                                }}
                            >
                                <div style={{
                                    background: '#d9e2ec', width: 50, height: 50,
                                    borderRadius: '50%', margin: '0 auto 1rem auto',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center'
                                }}>
                                    <User size={24} color="#627d98" />
                                </div>
                                <h3>{user.name}</h3>
                                <p style={{ fontSize: '0.9rem', color: '#486581' }}>{user.desc}</p>
                            </motion.div>
                        );
                    })}
                </div>
            )}

            {/* MODE: ASSESSMENT FORM */}
            {mode === 'assessment' && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="glass-panel"
                    style={{ maxWidth: '600px', margin: '0 auto 4rem auto', padding: '2rem' }}
                >
                    <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                        <ClipboardList size={40} color="#627d98" />
                        <h2>Current State Assessment</h2>
                        <p>Answer a few questions to get instant help.</p>
                    </div>

                    <form onSubmit={handleFormSubmit} style={{ display: 'grid', gridTemplateColumns: 'minmax(250px, 1fr) minmax(250px, 1fr)', gap: '1.5rem', alignItems: 'end' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Increasing Stress Levels?</label>
                            <select
                                style={{ width: '100%', padding: '0.8rem', borderRadius: '0.5rem', border: '1px solid #ccc' }}
                                value={formData.growing_stress}
                                onChange={(e) => setFormData({ ...formData, growing_stress: e.target.value })}
                            >
                                <option value="No">No</option>
                                <option value="Yes">Yes</option>
                            </select>
                        </div>

                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Mood Consistency?</label>
                            <select
                                style={{ width: '100%', padding: '0.8rem', borderRadius: '0.5rem', border: '1px solid #ccc' }}
                                value={formData.mood_swings}
                                onChange={(e) => setFormData({ ...formData, mood_swings: e.target.value })}
                            >
                                <option value="Low">Stable (Low Swings)</option>
                                <option value="Medium">Variable</option>
                                <option value="High">Volatile (High Swings)</option>
                            </select>
                        </div>

                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Social Difficulty?</label>
                            <select
                                style={{ width: '100%', padding: '0.8rem', borderRadius: '0.5rem', border: '1px solid #ccc' }}
                                value={formData.social_weakness}
                                onChange={(e) => setFormData({ ...formData, social_weakness: e.target.value })}
                            >
                                <option value="No">No</option>
                                <option value="Yes">Yes</option>
                            </select>
                        </div>

                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Coping Struggles?</label>
                            <select
                                style={{ width: '100%', padding: '0.8rem', borderRadius: '0.5rem', border: '1px solid #ccc' }}
                                value={formData.coping_struggles}
                                onChange={(e) => setFormData({ ...formData, coping_struggles: e.target.value })}
                            >
                                <option value="No">No</option>
                                <option value="Yes">Yes</option>
                            </select>
                        </div>

                        <div style={{ gridColumn: 'span 2' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>Interest in Work?</label>
                            <select
                                style={{ width: '100%', padding: '0.8rem', borderRadius: '0.5rem', border: '1px solid #ccc' }}
                                value={formData.work_interest}
                                onChange={(e) => setFormData({ ...formData, work_interest: e.target.value })}
                            >
                                <option value="Yes">Normal Interest</option>
                                <option value="No">Loss of Interest</option>
                            </select>
                        </div>

                        <motion.button
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                            type="submit"
                            style={{
                                gridColumn: 'span 2',
                                background: '#627d98', color: 'white', border: 'none',
                                padding: '1rem', borderRadius: '0.5rem', fontSize: '1rem', cursor: 'pointer', fontWeight: 'bold', marginTop: '1rem'
                            }}
                        >
                            Get Recommendations
                        </motion.button>
                    </form>
                </motion.div>
            )}

            {/* RESULTS GRAPH & CARDS */}
            <AnimatePresence>
                {loading && (
                    <motion.div
                        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                        style={{ textAlign: 'center', marginBottom: '2rem' }}
                    >
                        <p>Analyzing profile...</p>
                    </motion.div>
                )}

                {recommendations.length > 0 && (
                    <motion.div
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        {/* DYNAMIC RESULT GRAPH */}
                        <div className="glass-panel" style={{ marginBottom: '2rem', padding: '1rem', height: '400px', position: 'relative', overflow: 'hidden' }}>
                            <h3 style={{ textAlign: 'center', marginBottom: '1rem', color: '#627d98' }}>Logic Visualization</h3>
                            <ForceGraph2D
                                graphData={(function () {
                                    const nodes = [{ id: 'You', group: 'User', val: 10 }];
                                    const links = [];
                                    const conditions = new Set();

                                    recommendations.forEach(r => {
                                        if (!conditions.has(r.reason_category)) {
                                            conditions.add(r.reason_category);
                                            // Distinguish AI Match group
                                            const group = r.reason_category === 'AI Match' ? 'AIMatch' : 'Condition';
                                            nodes.push({ id: r.reason_category, group: group, val: 7 });
                                            links.push({ source: 'You', target: r.reason_category });
                                        }
                                        nodes.push({ id: r.title, group: 'Activity', val: 4 });
                                        links.push({ source: r.reason_category, target: r.title });
                                    });
                                    return { nodes, links };
                                })()}
                                nodeLabel="id"
                                nodeColor={node => {
                                    if (node.group === 'User') return '#627d98';
                                    if (node.group === 'Activity') return '#48bb78';
                                    if (node.group === 'AIMatch') return '#805ad5'; // Purple for AI
                                    return '#f6ad55';
                                }}
                                nodeRelSize={6}
                                linkColor={() => 'rgba(98, 125, 152, 0.3)'}
                                width={window.innerWidth > 800 ? 800 : window.innerWidth - 80}
                                height={320}
                                cooldownTicks={100}
                            />
                            <div style={{ position: 'absolute', top: 10, left: 10, background: 'rgba(255,255,255,0.8)', padding: '5px', borderRadius: '5px', fontSize: '0.8rem', pointerEvents: 'none' }}>
                                <div><span style={{ color: '#627d98' }}>●</span> You</div>
                                <div><span style={{ color: '#f6ad55' }}>●</span> Your Needs</div>
                                <div><span style={{ color: '#48bb78' }}>●</span> Suggested Solutions</div>
                            </div>
                        </div>

                        <h2 style={{ marginBottom: '2rem', textAlign: 'center' }}>Recommended Activities</h2>
                        <div className="grid-cards">
                            {recommendations.map((rec, index) => (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, x: -20 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.1 }}
                                    className="glass-panel"
                                    style={{ padding: '2rem' }}
                                >
                                    <div style={{
                                        display: 'flex', alignItems: 'center', gap: '0.5rem',
                                        marginBottom: '0.5rem', color: '#627d98', fontWeight: 800, fontSize: '0.8rem', textTransform: 'uppercase'
                                    }}>
                                        {rec.reason_category === 'Stress' && <Activity size={16} />}
                                        {rec.reason_category === 'MoodSwings' && <Brain size={16} />}
                                        {rec.reason_category === 'SocialWeakness' && <Users size={16} />}
                                        {rec.reason_category === 'Isolation' && <Sun size={16} />}
                                        {rec.reason_category === 'CopingIssues' && <Shield size={16} />}
                                        {rec.reason_category === 'WorkBurnout' && <Briefcase size={16} />}
                                        {rec.reason_category === 'WellBeing' && <Activity size={16} />}
                                        {rec.reason_category === 'AI Match' && <Sparkles size={16} color="#805ad5" />}
                                        {rec.reason_category}
                                    </div>

                                    <h3 style={{ margin: '0 0 1rem 0' }}>{rec.title}</h3>

                                    <div style={{
                                        background: 'rgba(98, 125, 152, 0.1)',
                                        padding: '1rem', borderRadius: '0.5rem',
                                        fontSize: '0.95rem', color: 'var(--text-muted)'
                                    }}>
                                        {rec.explanation}
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default App;
