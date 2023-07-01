import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Form from './Form'
import FooterInfo from './FooterInfo';
import { useRouter } from 'next/router';
import { useSimulation } from '../SimulationContext';

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

export default function Home() {
  const router = useRouter()
  const { setSimulationData } = useSimulation();
  const [anios, setAnios] = React.useState<string>('');
  const [dias, setDias] = React.useState<string>('');
  const [balanzas, setBalanzas] = React.useState<string>('');
  const [cantidadCamiones, setCantidadCamiones] = React.useState<string>('');
  const [activeSimulation, setActiveSimulation] = React.useState<boolean>(false);
  const actualizarCantidadAnios = (nuevoValor: string) => {
    setAnios(nuevoValor);
  };
  const actualizarCantidadDias = (nuevoValor: string) => {
    setDias(nuevoValor);
  };
  const actualizarCantidadBalanzas = (nuevoValor: string) => {
    setBalanzas(nuevoValor);
  };
  const actualizarCantidadCamiones = (nuevoValor: string) => {
    setCantidadCamiones(nuevoValor);
  };

  const realizarSimulacion = async () => {
    try {
      setActiveSimulation(true)
      const url = `http://localhost:8000?anios=${anios}&dias=${dias}&minutos=900&camiones=${cantidadCamiones}&cant_balanzas=${balanzas}`;
      console.log(`URL: ${url}`);
      const response = await fetch(url);
      const data = (await response.json()) as Anio[];
      console.log('Data');
      console.log(data);
      setSimulationData(data);
      setActiveSimulation(false);
      router.push('/simulation-result')
    } catch (error) {
      console.error('Error al realizar la llamada a la API:', error);
    }
  }

  return (
    <ThemeProvider theme={defaultTheme}>
      <CssBaseline />
      <AppBar
        position="absolute"
        color="default"
        elevation={0}
        sx={{
          position: 'relative',
          borderBottom: (t) => `1px solid ${t.palette.divider}`,
        }}
      >
        <Toolbar>
          <Typography variant="h6" color="inherit" noWrap>
            Modelos y Simulación - Trabajo Practico Final
          </Typography>
        </Toolbar>
      </AppBar>
      <Container component="main" maxWidth="sm" sx={{ mb: 4 }}>
        <Paper variant="outlined" sx={{ my: { xs: 3, md: 6 }, p: { xs: 2, md: 3 } }}>
          <Typography component="h1" variant="h4" align="center">
            Formulario de datos
          </Typography>
          <br/>
            <React.Fragment>
              <Form
                camiones={cantidadCamiones}
                actualizarCamiones={actualizarCantidadCamiones}
                anios={anios}
                actualizarAnios={actualizarCantidadAnios}
                dias={dias}
                actualizarDias={actualizarCantidadDias}
                balanzas={balanzas}
                actualizarBalanzas={actualizarCantidadBalanzas}
              />
              <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                {activeSimulation && (
                  <Box sx={{ mt: 3, ml: 1, display: 'flex', justifyContent: 'flex-end' }}>
                    <Typography variant="subtitle1">Simulacion en proceso...</Typography>
                    <br/>
                    <CircularProgress />
                  </Box>
                )}
                {!activeSimulation && (
                  <Button
                    variant="contained"
                    onClick={realizarSimulacion}
                    sx={{ mt: 3, ml: 1 }}
                  >
                    Simular
                  </Button>
                )}
              </Box>
            </React.Fragment>
        </Paper>
        {/* Footer */}
        <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer">
          <Typography variant="h6" align="center" gutterBottom>
            UNPSJB
          </Typography>
          <Typography
            variant="subtitle1"
            align="center"
            color="text.secondary"
            component="p"
          >
            Trabajo Practico Final
          </Typography>
          <FooterInfo />
        </Box>
        {/* End footer */}
      </Container>
    </ThemeProvider>
  );
}
