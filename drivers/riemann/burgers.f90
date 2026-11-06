! GAMS I2a2; scalar burgers interface checks.
! Upstream pin: 008d4921ea46878a97a96c8b8daa399a2e7b9078
program check_burgers
  implicit none
  interface
    subroutine rp1_ptwise(ne,na,nw,ql,qr,al,ar,w,s,am,ap)
      integer, intent(in) :: ne,na,nw
      real(kind=8), intent(inout) :: ql(ne),qr(ne),al(na),ar(na)
      real(kind=8), intent(inout) :: w(ne,nw),s(nw),am(ne),ap(ne)
    end subroutine
  end interface
  real(kind=8) :: ql(1),qr(1),al(1),ar(1),w(1,1),s(1),am(1),ap(1)
  real(kind=8), parameter :: left(8) =[1d0,-3d0,-2d0,1d0,2d0,1d0,2d0,0d0]
  real(kind=8), parameter :: right(8)=[3d0,-1d0,1d0,-1d0,-1d0,-2d0,2d0,0d0]
  real(kind=8) :: fl,fr,flux,err,maxerr,tol
  integer :: i
  maxerr=0d0; al=0d0; ar=0d0
  do i=1,size(left)
    ql=left(i); qr=right(i); w=0d0; s=0d0; am=0d0; ap=0d0
    call rp1_ptwise(1,1,1,ql,qr,al,ar,w,s,am,ap)
    fl=0.5d0*left(i)**2; fr=0.5d0*right(i)**2
    ! Independent exact Godunov flux from the scalar Riemann solution.
    if(left(i)>right(i))then
      flux=max(fl,fr)
    elseif(left(i)>=0d0)then
      flux=fl
    elseif(right(i)<=0d0)then
      flux=fr
    else
      flux=0d0
    endif
    err=max(abs(fl+am(1)-flux),abs(fr-ap(1)-flux), &
            abs(am(1)+ap(1)-(fr-fl)), &
            abs(w(1,1)-(right(i)-left(i))), &
            abs(s(1)-0.5d0*(left(i)+right(i))))
    tol=2d-13*max(1d0,abs(fl),abs(fr),abs(flux))
    if(.not.(err<=tol))error stop 'Burgers Godunov flux/entropy check failed'
    maxerr=max(maxerr,err)
  enddo
  print '(a,es12.4)','Maximum absolute error: ',maxerr
  print '(a)','PASS Burgers: 8 shock, rarefaction, transonic and constant-state cases'
end program check_burgers
