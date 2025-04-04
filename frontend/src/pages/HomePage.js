import React, { useEffect, useState } from 'react';
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography, CircularProgress, Box
} from '@mui/material';

function HashtagTable() {
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTrends = async () => {
    try {
      const response = await fetch('/api/get-trends');
      const data = await response.json();
      setTrends(data);
    } catch (error) {
      console.error('Failed to fetch trends:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTrends(); // Initial load

    const interval = setInterval(() => {
      fetchTrends();
    }, 30000); // Poll every 30 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" gutterBottom>
        Trending Hashtags
      </Typography>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <TableContainer component={Paper}>
          <Table aria-label="trending hashtags">
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
                trends.map((trend, index) => (
                  <TableRow key={index}>
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>{trend.hashtag}</TableCell>
                    <TableCell>{trend.count}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
}

export default HashtagTable;
