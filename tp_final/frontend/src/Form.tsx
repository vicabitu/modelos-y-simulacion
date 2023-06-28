import React, { ChangeEvent } from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import InputLabel from '@mui/material/InputLabel';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

interface Props {
  actualizarCamiones: (nuevaCantidad: string) => void;
  camiones: string;
  actualizarAnios: (nuevaCantidad: string) => void;
  anios: string;
  actualizarDias: (nuevaCantidad: string) => void;
  dias: string;
  actualizarHoras: (nuevaCantidad: string) => void;
  horas: string;
}

export default function Form({
  actualizarCamiones,
  camiones,
  actualizarAnios,
  anios,
  actualizarHoras,
  horas,
  actualizarDias,
  dias
  }: Props) {
  const handleChangeCamiones = (event: ChangeEvent<HTMLInputElement>) => {
    actualizarCamiones(event.target.value)
  };
  // console.log(`Form - Cantidad de camiones: ${camiones}`)
  const handleChangeAnios = (event: ChangeEvent<HTMLInputElement>) => {
    actualizarAnios(event.target.value)
  };
  // console.log(`Form - Cantidad de anios: ${anios}`)
  const handleChangeHoras = (event: ChangeEvent<HTMLInputElement>) => {
    actualizarHoras(event.target.value)
  };
  // console.log(`Form - Cantidad de horas: ${horas}`)
  const handleChangeDias = (event: ChangeEvent<HTMLInputElement>) => {
    actualizarDias(event.target.value)
  };
  // console.log(`Form - Cantidad de dias: ${dias}`)
  return (
    <React.Fragment>
      <Typography variant="h6" gutterBottom>
        Ingrese los datos para la simulación
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="anios"
            name="anios"
            label="Años"
            fullWidth
            variant="standard"
            type="number"
            onChange={handleChangeAnios}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="dias"
            name="dias"
            label="Dias"
            fullWidth
            variant="standard"
            type="number"
            onChange={handleChangeDias}
          />
        </Grid>
        {/* <Grid item xs={12}>
          <InputLabel id="select-camiones-label">Cantidad de camiones</InputLabel>
          <Select
            labelId="select-camiones-label"
            id="select-camiones"
            value={camiones}
            onChange={handleChangeCamiones}
            label="Cantidad de camiones"
            fullWidth
          >
            <MenuItem value={5}>Cinco</MenuItem>
            <MenuItem value={10}>Diez</MenuItem>
            <MenuItem value={15}>Quince</MenuItem>
          </Select>
        </Grid> */}
        {/* <Grid item xs={12}>
          <TextField
            id="address2"
            name="address2"
            label="Address line 2"
            fullWidth
            autoComplete="shipping address-line2"
            variant="standard"
          />
        </Grid> */}
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="horas"
            name="horas"
            label="Horas"
            fullWidth
            autoComplete="shipping address-level2"
            variant="standard"
            type="number"
            onChange={handleChangeHoras}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            id="camiones"
            name="camiones"
            label="Camiones"
            fullWidth
            variant="standard"
            type="number"
            onChange={handleChangeCamiones}
          />
        </Grid>
        {/*<Grid item xs={12} sm={6}>
          <TextField
            required
            id="zip"
            name="zip"
            label="Zip / Postal code"
            fullWidth
            autoComplete="shipping postal-code"
            variant="standard"
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            required
            id="country"
            name="country"
            label="Country"
            fullWidth
            autoComplete="shipping country"
            variant="standard"
          />
        </Grid>
        <Grid item xs={12}>
          <FormControlLabel
            control={<Checkbox color="secondary" name="saveAddress" value="yes" />}
            label="Use this address for payment details"
          />
        </Grid> */}
      </Grid>
    </React.Fragment>
  );
}
