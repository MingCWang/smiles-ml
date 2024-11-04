// @ts-expect-error - ignore the error for import meta
import './App.css';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import { useState } from 'react';


function App() {
	// @ts-expect-error - ignore the error for import meta
	const SERVER_URL = import.meta.env.VITE_SERVER_URL as string;
	const [smiles, setSmiles] = useState('');
	const [predictions, setPredictions] = useState('');
	const [isValidSmiles, setIsValidSmiles] = useState(false);
	const [results, setResults] = useState<{ smiles: string; predictions: string; is_valid_smile: boolean }[]>([]);
	const [isLoading, setIsLoading] = useState(false);

	const [error, setError] = useState('');
	// @ts-expect-error - ignore the error for import meta
	const handleGenerateTen = async (event) => {
		setPredictions('');
		setSmiles('');
		setIsValidSmiles(false);
		setIsLoading(true);
		setError('');

		event.preventDefault(); // Prevent default form submission behavior
		// Send SMILES data to the backend
		fetch(`${SERVER_URL}/results?result_num=1`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			}
		})
			.then((response) => response.json())
			.then((data) => {
				console.log('Success:', data);
				setResults(data.results);
				setIsLoading(false);
			})
			.catch((error) => {
				setError(error);
				setIsLoading(false);

			});
	}
	// Handle form submission
	// @ts-expect-error - ignore the error for import meta
	const handleSubmit = async (event) => {
		setResults([]);
		event.preventDefault(); // Prevent default form submission behavior
		// Send SMILES data to the backend
		fetch(`${SERVER_URL}/predict?smiles=${encodeURIComponent(smiles)}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
		})
			// Check if the response is successful
			.then((response) => response.json())
			.then((data) => {
				console.log('Success:', data);
				setPredictions(data.predictions);
				setIsValidSmiles(data.is_valid_smile);
			})
			.catch((error) => {
				setError(error);
			});
	}
	// O=C([C@@H](c1ccc(cc1)O)N)N[C@@H]1C(=O)N2[C@@H]1SC([C@@H]2C(=O)O)(C)C
	return (
		<>
			<div className="container">
				<div className='title'>Prediction and Visualization from SMILES data</div>
				<div className="inputContainer">
					<TextField id="outlined-basic" value={smiles} onChange={(e) => setSmiles(e.target.value)} placeholder="input smile string" variant="outlined" className='input' sx={{
						input: { color: 'white' }
					}} />
					<Button variant="contained" onClick={handleSubmit} sx={{ margin: 'auto 10px', height: 40 }}>submit</Button>

				</div>
				<p>or</p>
				<Button variant="contained" onClick={handleGenerateTen} sx={{ height: 40, width: 300 }}>generate random results</Button>


			</div>


			<div className="resultContainer">
				<div className='title'>Results</div>
				{!isLoading ?
					<>
						{error && <div className='error'>{error}</div>}
						
						<>
							{predictions && <>
								<img src={`${SERVER_URL}/plot?to_plot=${predictions}`} alt="Plot" />
								<img src={`${SERVER_URL}/mol_image?smiles=${smiles}`} alt="Molecule Image" />

							</>}
							{results &&
								<div className='results'>
									{results.map((result, index) => (
										<div key={index} className='result'>
											<div className='smiles'>{result.smiles}</div>
											{result.is_valid_smile ?
												<>
													<img src={`${SERVER_URL}/plot?to_plot=${result.predictions}`} alt="Plot" />
													<img src={`${SERVER_URL}/mol_image?smiles=${result.smiles}`} alt="Molecule Image" />
												</>
												: <div className='error'>Invalid SMILES string</div>}
										</div>
									))}
								</div>}

						</>
							{!isValidSmiles && <div className='error'>Invalid SMILES string</div>}
					</>
					: <div className='loading'>Loading...</div>
				}
			</div>
		</>

	)
}

export default App
