import React, { useEffect, useState } from 'react';
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography,
  CircularProgress, Box, Grid, TextField,
  IconButton, Button
} from '@mui/material';
import { Add, Delete } from '@mui/icons-material';
import Graph from './UploadPage.js';

function HashtagTable() {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [customTrends, setCustomTrends] = useState({});

  const fetchTrends = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/get-trends');
      const data = await response.json();
      console.log('data --> ', data);
      if(data.length !== 0){
        setTrends(data);
      }
      console.log('hi --')
    } catch (error) {
      console.error('Failed to fetch trends:', error);
    } finally {
      setLoading(false);
    }
  };
  const handleAddTrend = () => {

    setCustomTrends({ ...customTrends, '': '' });
  };

  const handleKeyChange = (oldKey, newKey) => {
    const updated = { ...customTrends };
    const value = updated[oldKey];
    delete updated[oldKey];
    updated[newKey] = value;
    setCustomTrends(updated);
  };

  const handleValueChange = (key, value) => {
    setCustomTrends({ ...customTrends, [key]: value });
  };

  const handleDelete = (key) => {
    const updated = { ...customTrends };
    delete updated[key];
    setCustomTrends(updated);
  };

  const handleUpdate = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/update-trends', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(customTrends),
      });

      if (response.ok) {
        alert('Trends updated successfully');
        // fetchTrends();
      } else {
        alert('Update failed');
      }
    } catch (error) {
      console.error('Error updating trends:', error);
      alert('Error updating trends');
    }
  };

  useEffect(() => {
    fetchTrends();
    const interval = setInterval(fetchTrends, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ padding: 4 }}>
      <Grid container spacing={2}>
        {/* Left Side - Table */}
        <Grid item xs={12} md={7}>
          <Typography variant="h4" gutterBottom>
            Trending Hashtags
          </Typography>

          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <CircularProgress />
            </Box>
          ) : (
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>#</TableCell>
                    <TableCell>Hashtag</TableCell>
                    <TableCell>Count</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {trends.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={3} align="center">
                        No data available
                      </TableCell>
                    </TableRow>
                  ) : (
                    trends.map((t, index) => (
                      <TableRow key={index}>
                        <TableCell>{index + 1}</TableCell>
                        <TableCell>{t.hashtag}</TableCell>
                        <TableCell>{t.count}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          )}
          <div style={{width:'400px'}}>
            <Graph/>
          </div>
        </Grid>

        {/* Right Side - Form */}
        <Grid item xs={12} md={5}>
          <Typography variant="h5" gutterBottom>
            Add / Edit Hashtags
          </Typography>

          {Object.entries(customTrends).map(([hashtag, weight], index) => (
            <Box key={index} sx={{ display: 'flex', mb: 2, gap: 1 }}>
              <TextField
                label="Hashtag"
                fullWidth
                value={hashtag}
                onChange={(e) => handleKeyChange(hashtag, e.target.value)}
              />
              <TextField
                label="Weight"
                type="number"
                value={weight}
                onChange={(e) => handleValueChange(hashtag, e.target.value)}
              />
              <IconButton onClick={() => handleDelete(hashtag)} color="error">
                <Delete />
              </IconButton>
            </Box>
          ))}

          <Button
            variant="outlined"
            startIcon={<Add />}
            onClick={handleAddTrend}
            sx={{ mt: 2 }}
          >
            Add Hashtag
          </Button>

          {Object.keys(customTrends).length > 0 && (
            <Button
              variant="contained"
              onClick={handleUpdate}
              sx={{ mt: 2, ml: 2 }}
            >
              Update Trends
            </Button>
          )}
        </Grid>
      </Grid>
    </Box>
  );
}

export default HashtagTable;
