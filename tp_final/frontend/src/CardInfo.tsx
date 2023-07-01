import * as React from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import Title from './Title';

interface Props {
  titulo: string;
  valor: number
}

export default function CardInfo({titulo, valor}: Props) {
  return (
    <React.Fragment>
      <Title>{titulo}</Title>
      <Typography component="p" variant="h4">
        {valor}
      </Typography>
    </React.Fragment>
  );
}
