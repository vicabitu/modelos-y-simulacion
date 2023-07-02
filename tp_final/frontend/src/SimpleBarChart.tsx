import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import { BarChart, CartesianGrid, Bar, Tooltip, XAxis, YAxis, ResponsiveContainer } from 'recharts';
import Title from './Title';

interface Props {
  data: { name: number; value: number }[];
  title: string
}

export default function SimpleBarChart({ data, title }: Props) {
  const theme = useTheme();

  return (
    <React.Fragment>
      <Title>{title}</Title>
      <ResponsiveContainer>
        <BarChart
          data={data}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </React.Fragment>
  );
}
