import React, { ChangeEvent } from 'react';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';

export default function FooterInfo() {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {/* {'Copyright © '} */}
      <Link color="inherit" href="#">
        Victor Andres Abitú
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
  </Typography>
  )
}