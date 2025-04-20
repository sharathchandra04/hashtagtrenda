import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { MultiSelect } from "react-multi-select-component";
import {
  Table, TableBody, TableCell, TableContainer,
  TableHead, TableRow, Paper, Typography,
  CircularProgress, Box, Grid, TextField,
  IconButton, Button
} from '@mui/material';

const HashtagTrendChart = () => {
  const [dataList, setDataList] = useState([]); // list of objects
  const [hashtagOptions, setHashtagOptions] = useState([]); // dropdown options
  const [selectedHashtags, setSelectedHashtags] = useState([]); // selected hashtags
  const [hashtag, setHashtag] = useState(''); // selected hashtags

  // Polling every 10 seconds
  useEffect(() => {
    const interval = setInterval(fetchData, 10000);
    fetchData(); // initial fetch
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/hashtags?hashtag=${hashtag}`);
      const result = await response.json(); // expected format: { "#hashtag1": 10, "#hashtag2": 25, ... }
      const timestamp = new Date().toLocaleTimeString();

      const newEntry = { time: timestamp, ...result };

      setDataList((prevList) => {
        const updatedList = [...prevList, newEntry];
        return updatedList.length > 25 ? updatedList.slice(-25) : updatedList;
      });

      // const uniqueHashtags = Object.keys(result);
      // const options = uniqueHashtags.map((tag) => ({ label: tag, value: tag }));
      // setHashtagOptions((prevOptions) => {
      //   const allOptions = new Set([...prevOptions.map(o => o.value), ...uniqueHashtags]);
      //   return Array.from(allOptions).map(tag => ({ label: tag, value: tag }));
      // });
    } catch (err) {
      console.error("Error fetching hashtag data:", err);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Hashtag Trend Chart</h2>

      {/* <MultiSelect
        style={{width:'100px'}}
        options={hashtagOptions}
        value={selectedHashtags}
        onChange={setSelectedHashtags}
        labelledBy="Select Hashtags"
        className="mb-4"
      /> */}
      <Box sx={{ display: 'flex', mb: 2, gap: 1 }}>
        <TextField
          label="Hashtag"
          fullWidth
          value={hashtag}
          onChange={(e) => {setHashtag(e.target.value); setDataList([])}}
        />
      </Box>

      <LineChart
        width={900}
        height={400}
        data={dataList}
        margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          key={hashtag}
          type="monotone"
          dataKey={hashtag}
          stroke={"##0000FF"}
          strokeWidth={2}
          dot={false}
        />
        {/* {selectedHashtags.slice(0, 1).map((tag, index) => (
        ))} */}
      </LineChart>
    </div>
  );
};

export default HashtagTrendChart;
