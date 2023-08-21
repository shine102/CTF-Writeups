FROM node:14

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./src/ .

RUN npm install

ENV FLAG="FUSec{ch0n_lu0ng_FBTU_hoc_ph1_29_cu}"
ENV JWT_SECRET_KEY="BI_MAT_KO_THE_BAT_MI"

RUN echo "FUSec{ch1_c0_ngu_m0i_n0p_c4i_fl4g_tr3n_k1a}" > /flag
RUN chmod 0400 /flag
COPY ./getFlag.c /getFlag.c
RUN gcc /getFlag.c -o /getFlag
RUN chmod 4755 /getFlag

EXPOSE 3000

CMD [ "node", "index.js" ]