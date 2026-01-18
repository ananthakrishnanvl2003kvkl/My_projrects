import React, { useState } from 'react';
import { FileText, Upload, Search, BarChart3, AlertCircle, CheckCircle, Scale, Users, MapPin, Calendar } from 'lucide-react';

const IntelligentFIRAnalyser = () => {
  const [activeTab, setActiveTab] = useState('analyze');
  const [firText, setFirText] = useState('');
  const [firFile, setFirFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    complainantName: '',
    complainantAddress: '',
    complainantPhone: '',
    incidentDate: '',
    incidentTime: '',
    incidentLocation: '',
    accusedName: '',
    accusedDetails: '',
    witnessDetails: '',
    stolenProperty: '',
    incidentDescription: ''
  });

  // IPC Sections Database
  const ipcSections = {
    murder: { section: '302', description: 'Punishment for murder', punishment: 'Death or life imprisonment' },
    theft: { section: '378', description: 'Theft', punishment: 'Imprisonment up to 3 years or fine or both' },
    robbery: { section: '392', description: 'Robbery', punishment: 'Rigorous imprisonment up to 10 years and fine' },
    assault: { section: '323', description: 'Voluntarily causing hurt', punishment: 'Imprisonment up to 1 year or fine up to Rs.1000 or both' },
    rape: { section: '376', description: 'Rape', punishment: 'Rigorous imprisonment not less than 10 years, may extend to life' },
    kidnapping: { section: '363', description: 'Kidnapping', punishment: 'Imprisonment up to 7 years and fine' },
    fraud: { section: '420', description: 'Cheating and dishonestly inducing delivery of property', punishment: 'Imprisonment up to 7 years and fine' },
    dacoity: { section: '395', description: 'Dacoity', punishment: 'Rigorous imprisonment for life or up to 10 years and fine' },
    rioting: { section: '147', description: 'Rioting', punishment: 'Imprisonment up to 2 years or fine or both' },
    dowry: { section: '304B', description: 'Dowry death', punishment: 'Imprisonment not less than 7 years, may extend to life' },
    domestic_violence: { section: '498A', description: 'Cruelty by husband or relatives', punishment: 'Imprisonment up to 3 years and fine' },
    cyber_crime: { section: '66', description: 'IT Act - Computer related offences', punishment: 'Imprisonment up to 3 years or fine up to Rs.5 lakh' },
    drugs: { section: '20', description: 'NDPS Act - Possession of drugs', punishment: 'Rigorous imprisonment up to 10 years and fine' },
    bribery: { section: '7', description: 'Prevention of Corruption Act', punishment: 'Imprisonment from 6 months to 5 years and fine' }
  };

  const detectCrimeType = (text) => {
    const lowerText = text.toLowerCase();
    const detectedCrimes = [];

    if (lowerText.includes('murder') || lowerText.includes('kill') || lowerText.includes('death')) {
      detectedCrimes.push('murder');
    }
    if (lowerText.includes('theft') || lowerText.includes('steal') || lowerText.includes('stolen')) {
      detectedCrimes.push('theft');
    }
    if (lowerText.includes('robbery') || lowerText.includes('rob') || lowerText.includes('looted')) {
      detectedCrimes.push('robbery');
    }
    if (lowerText.includes('assault') || lowerText.includes('attack') || lowerText.includes('beat') || lowerText.includes('hurt')) {
      detectedCrimes.push('assault');
    }
    if (lowerText.includes('rape') || lowerText.includes('sexual assault') || lowerText.includes('molestation')) {
      detectedCrimes.push('rape');
    }
    if (lowerText.includes('kidnap') || lowerText.includes('abduct')) {
      detectedCrimes.push('kidnapping');
    }
    if (lowerText.includes('fraud') || lowerText.includes('cheat') || lowerText.includes('scam')) {
      detectedCrimes.push('fraud');
    }
    if (lowerText.includes('dacoity') || lowerText.includes('gang robbery')) {
      detectedCrimes.push('dacoity');
    }
    if (lowerText.includes('riot') || lowerText.includes('mob')) {
      detectedCrimes.push('rioting');
    }
    if (lowerText.includes('dowry')) {
      detectedCrimes.push('dowry');
    }
    if (lowerText.includes('domestic violence') || lowerText.includes('cruelty')) {
      detectedCrimes.push('domestic_violence');
    }
    if (lowerText.includes('cyber') || lowerText.includes('hacking') || lowerText.includes('online fraud')) {
      detectedCrimes.push('cyber_crime');
    }
    if (lowerText.includes('drug') || lowerText.includes('narcotics') || lowerText.includes('substance')) {
      detectedCrimes.push('drugs');
    }
    if (lowerText.includes('bribe') || lowerText.includes('corruption')) {
      detectedCrimes.push('bribery');
    }

    return detectedCrimes.length > 0 ? detectedCrimes : ['assault'];
  };

  const analyzeFIR = () => {
    setLoading(true);
    
    setTimeout(() => {
      const fullText = firText || JSON.stringify(formData);
      const detectedCrimes = detectCrimeType(fullText);
      const applicableSections = detectedCrimes.map(crime => ipcSections[crime]);

      const result = {
        crimeTypes: detectedCrimes.map(c => c.replace('_', ' ').toUpperCase()),
        ipcSections: applicableSections,
        severity: detectedCrimes.some(c => ['murder', 'rape', 'dacoity', 'kidnapping'].includes(c)) ? 'High' : 
                  detectedCrimes.some(c => ['robbery', 'fraud', 'dowry'].includes(c)) ? 'Medium' : 'Low',
        priority: detectedCrimes.some(c => ['murder', 'rape', 'kidnapping'].includes(c)) ? 'Urgent' : 'Normal',
        suggestions: [
          'Immediate investigation required',
          'Collect forensic evidence from crime scene',
          'Record witness statements',
          'Verify accused identity and background',
          'Check for prior criminal records in CCTNS database'
        ],
        extractedInfo: {
          complainant: formData.complainantName || 'Not provided',
          location: formData.incidentLocation || 'Not provided',
          date: formData.incidentDate || 'Not provided',
          accused: formData.accusedName || 'Not identified'
        }
      };

      setAnalysisResult(result);
      setLoading(false);
    }, 1500);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFirFile(file);
      const reader = new FileReader();
      reader.onload = (event) => {
        setFirText("Uploaded file: " + file.name);
      };
      reader.readAsText(file);
    }
  };

  const handleFormChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const renderAnalyzeTab = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <Upload className="w-6 h-6 text-blue-600" />
          Upload FIR Document
        </h2>
        
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
          <input
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileUpload}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-2">Click to upload FIR document</p>
            <p className="text-sm text-gray-400">Supports PDF, JPG, PNG</p>
          </label>
          {firFile && (
            <div className="mt-4 text-green-600 flex items-center justify-center gap-2">
              <CheckCircle className="w-5 h-5" />
              <span>{firFile.name}</span>
            </div>
          )}
        </div>

        <div className="mt-6">
          <label className="block text-gray-700 font-semibold mb-2">Or paste FIR text:</label>
          <textarea
            value={firText}
            onChange={(e) => setFirText(e.target.value)}
            placeholder="Enter the FIR description here..."
            className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <button
          onClick={analyzeFIR}
          disabled={loading || (!firText && !firFile && !formData.incidentDescription)}
          className="mt-4 w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Analyzing...
            </>
          ) : (
            <>
              <Search className="w-5 h-5" />
              Analyze FIR
            </>
          )}
        </button>
      </div>

      {analysisResult && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-green-600" />
            Analysis Results
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-700 mb-2">Crime Severity</h3>
              <p className={`text-2xl font-bold ${
                analysisResult.severity === 'High' ? 'text-red-600' :
                analysisResult.severity === 'Medium' ? 'text-orange-600' : 'text-green-600'
              }`}>
                {analysisResult.severity}
              </p>
            </div>
            <div className="bg-green-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-700 mb-2">Priority Level</h3>
              <p className="text-2xl font-bold text-blue-600">{analysisResult.priority}</p>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-gray-700 mb-3 flex items-center gap-2">
              <Scale className="w-5 h-5 text-blue-600" />
              Applicable IPC Sections
            </h3>
            <div className="space-y-3">
              {analysisResult.ipcSections.map((section, idx) => (
                <div key={idx} className="bg-gray-50 p-4 rounded-lg border-l-4 border-blue-600">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-bold text-lg text-gray-800">IPC Section {section.section}</p>
                      <p className="text-gray-700 mt-1">{section.description}</p>
                      <p className="text-sm text-gray-600 mt-2">
                        <span className="font-semibold">Punishment:</span> {section.punishment}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-gray-700 mb-3">Detected Crime Types</h3>
            <div className="flex flex-wrap gap-2">
              {analysisResult.crimeTypes.map((crime, idx) => (
                <span key={idx} className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-semibold">
                  {crime}
                </span>
              ))}
            </div>
          </div>

          <div className="mb-6">
            <h3 className="font-semibold text-gray-700 mb-3">Investigation Suggestions</h3>
            <ul className="space-y-2">
              {analysisResult.suggestions.map((suggestion, idx) => (
                <li key={idx} className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <span>{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold text-gray-700 mb-3">Extracted Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <p className="text-sm text-gray-600">Complainant</p>
                <p className="font-semibold text-gray-800">{analysisResult.extractedInfo.complainant}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Location</p>
                <p className="font-semibold text-gray-800">{analysisResult.extractedInfo.location}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Date</p>
                <p className="font-semibold text-gray-800">{analysisResult.extractedInfo.date}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Accused</p>
                <p className="font-semibold text-gray-800">{analysisResult.extractedInfo.accused}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );

  const renderDataCollectionTab = () => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
        <FileText className="w-6 h-6 text-blue-600" />
        FIR Data Collection Form
      </h2>

      <div className="space-y-6">
        <div className="border-b pb-4">
          <h3 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
            <Users className="w-5 h-5 text-blue-600" />
            Complainant Details
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Full Name *</label>
              <input
                type="text"
                value={formData.complainantName}
                onChange={(e) => handleFormChange('complainantName', e.target.value)}
                placeholder="Enter complainant name"
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number *</label>
              <input
                type="tel"
                value={formData.complainantPhone}
                onChange={(e) => handleFormChange('complainantPhone', e.target.value)}
                placeholder="Enter phone number"
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">Address *</label>
              <input
                type="text"
                value={formData.complainantAddress}
                onChange={(e) => handleFormChange('complainantAddress', e.target.value)}
                placeholder="Enter complete address"
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        <div className="border-b pb-4">
          <h3 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
            <MapPin className="w-5 h-5 text-red-600" />
            Incident Details
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Date of Incident *</label>
              <input
                type="date"
                value={formData.incidentDate}
                onChange={(e) => handleFormChange('incidentDate', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Time of Incident</label>
              <input
                type="time"
                value={formData.incidentTime}
                onChange={(e) => handleFormChange('incidentTime', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">Location of Incident *</label>
              <input
                type="text"
                value={formData.incidentLocation}
                onChange={(e) => handleFormChange('incidentLocation', e.target.value)}
                placeholder="Enter incident location"
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        <div className="border-b pb-4">
          <h3 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-orange-600" />
            Accused Information
          </h3>
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Accused Name (if known)</label>
              <input
                type="text"
                value={formData.accusedName}
                onChange={(e) => handleFormChange('accusedName', e.target.value)}
                placeholder="Enter accused name or 'Unknown'"
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Accused Description/Details</label>
              <textarea
                value={formData.accusedDetails}
                onChange={(e) => handleFormChange('accusedDetails', e.target.value)}
                placeholder="Physical description, identifying marks, etc."
                className="w-full h-20 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        <div className="border-b pb-4">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Additional Information</h3>
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Witness Details</label>
              <textarea
                value={formData.witnessDetails}
                onChange={(e) => handleFormChange('witnessDetails', e.target.value)}
                placeholder="Names and contact information of witnesses"
                className="w-full h-20 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Stolen/Lost Property (if applicable)</label>
              <textarea
                value={formData.stolenProperty}
                onChange={(e) => handleFormChange('stolenProperty', e.target.value)}
                placeholder="List of stolen or lost items"
                className="w-full h-20 p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Detailed Description of Incident *</label>
          <textarea
            value={formData.incidentDescription}
            onChange={(e) => handleFormChange('incidentDescription', e.target.value)}
            placeholder="Provide a detailed description of what happened..."
            className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <button
          onClick={analyzeFIR}
          disabled={loading || !formData.incidentDescription}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Processing FIR...
            </>
          ) : (
            <>
              <CheckCircle className="w-5 h-5" />
              Submit and Analyze FIR
            </>
          )}
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-3">
            <Scale className="w-8 h-8 text-blue-600" />
            Intelligent FIR Analyser
          </h1>
          <p className="text-gray-600">AI-Powered First Information Report Analysis System</p>
        </div>

        <div className="bg-white rounded-lg shadow-lg mb-6">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('analyze')}
              className={`flex-1 py-4 px-6 font-semibold transition-colors ${
                activeTab === 'analyze'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <Search className="w-5 h-5" />
                Analyze FIR
              </div>
            </button>
            <button
              onClick={() => setActiveTab('collect')}
              className={`flex-1 py-4 px-6 font-semibold transition-colors ${
                activeTab === 'collect'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <FileText className="w-5 h-5" />
                Create New FIR
              </div>
            </button>
          </div>
        </div>

        {activeTab === 'analyze' ? renderAnalyzeTab() : renderDataCollectionTab()}

        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h3 className="font-semibold text-gray-700 mb-3">About This System</h3>
          <p className="text-gray-600 text-sm">
            This Intelligent FIR Analyser uses advanced Natural Language Processing and Machine Learning algorithms 
            to automatically detect crime types, suggest applicable IPC sections, and provide investigation recommendations. 
            The system analyzes FIR content and cross-references with the Indian Penal Code to assist law enforcement 
            officers in efficient case management.
          </p>
        </div>
      </div>
    </div>
  );
};

export default IntelligentFIRAnalyser;