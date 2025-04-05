import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { MultiSelect } from "react-multi-select-component";

const HashtagTrendChart = () => {
  const [dataList, setDataList] = useState([]); // list of objects
  const [hashtagOptions, setHashtagOptions] = useState([]); // dropdown options
  const [selectedHashtags, setSelectedHashtags] = useState([]); // selected hashtags

  // Polling every 10 seconds
  useEffect(() => {
    const interval = setInterval(fetchData, 10000);
    fetchData(); // initial fetch
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/hashtags");
      const result = await response.json(); // expected format: { "#hashtag1": 10, "#hashtag2": 25, ... }
      const timestamp = new Date().toLocaleTimeString();

      const newEntry = { time: timestamp, ...result };

      setDataList((prevList) => {
        const updatedList = [...prevList, newEntry];
        return updatedList.length > 25 ? updatedList.slice(-25) : updatedList;
      });

      // Update dropdown options
      const uniqueHashtags = Object.keys(result);
      const options = uniqueHashtags.map((tag) => ({ label: tag, value: tag }));
      setHashtagOptions((prevOptions) => {
        const allOptions = new Set([...prevOptions.map(o => o.value), ...uniqueHashtags]);
        return Array.from(allOptions).map(tag => ({ label: tag, value: tag }));
      });
    } catch (err) {
      console.error("Error fetching hashtag data:", err);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Hashtag Trend Chart</h2>

      <MultiSelect
        style={{width:'100px'}}
        options={hashtagOptions}
        value={selectedHashtags}
        onChange={setSelectedHashtags}
        labelledBy="Select Hashtags"
        className="mb-4"
      />

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
        {selectedHashtags.slice(0, 5).map((tag, index) => (
          <Line
            key={tag.value}
            type="monotone"
            dataKey={tag.value}
            stroke={"#" + ((Math.random() * 0xffffff) << 0).toString(16)}
            strokeWidth={2}
            dot={false}
          />
        ))}
      </LineChart>
    </div>
  );
};

export default HashtagTrendChart;
